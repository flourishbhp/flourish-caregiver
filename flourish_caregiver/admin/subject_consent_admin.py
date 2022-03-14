from _collections import OrderedDict
import datetime
from functools import partialmethod
import uuid

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from edc_consent.actions import (
    flag_as_verified_against_paper, unflag_as_verified_against_paper)
from edc_constants.constants import MALE, FEMALE
from edc_model_admin import ModelAdminBasicMixin
from edc_model_admin import ModelAdminFormAutoNumberMixin, audit_fieldset_tuple, audit_fields
from edc_model_admin import StackedInlineMixin
from simple_history.admin import SimpleHistoryAdmin
import xlwt

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverChildConsentForm, SubjectConsentForm
from ..models import CaregiverChildConsent, SubjectConsent
from ..models import ScreeningPregWomen
from .modeladmin_mixins import ModelAdminMixin


class CaregiverChildConsentInline(StackedInlineMixin, ModelAdminFormAutoNumberMixin,
                                  admin.StackedInline):
    model = CaregiverChildConsent
    form = CaregiverChildConsentForm

    extra = 0
    max_num = 3

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'study_child_identifier',
                'first_name',
                'last_name',
                'gender',
                'child_dob',
                'child_test',
                'child_remain_in_study',
                'child_preg_test',
                'child_knows_status',
                'identity',
                'identity_type',
                'confirm_identity',
                'future_studies_contact',
                'specimen_consent',
                'consent_datetime'
            ]}
         ),)

    radio_fields = {'gender': admin.VERTICAL,
                    'child_test': admin.VERTICAL,
                    'child_remain_in_study': admin.VERTICAL,
                    'child_preg_test': admin.VERTICAL,
                    'child_knows_status': admin.VERTICAL,
                    'identity_type': admin.VERTICAL,
                    'specimen_consent': admin.VERTICAL,
                    'future_studies_contact': admin.VERTICAL}

    child_dataset_cls = django_apps.get_model('flourish_child.childdataset')
    preg_women_cls = django_apps.get_model('flourish_caregiver.screeningpregwomen')
    consent_cls = django_apps.get_model('flourish_caregiver.caregiverchildconsent')

    def save_model(self, request, obj, form, change):
        super(CaregiverChildConsentInline, self).save_model(request, obj, form, change)

    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        study_maternal_id = request.GET.get('study_maternal_identifier')
        if study_maternal_id:
            child_datasets = self.child_dataset_cls.objects.filter(
                study_maternal_identifier=study_maternal_id)
            genders = {'Male': MALE, 'Female': FEMALE}
            if obj:
                child_datasets = self.get_difference(child_datasets, obj)

            for child in child_datasets:
                initial.append({
                    'study_child_identifier': child.study_child_identifier,
                    'gender': genders.get(child.infant_sex),
                    'child_dob': child.dob
                })

        subject_identifier = request.GET.get('subject_identifier')
        screening_identifier = request.GET.get('screening_identifier')

        if subject_identifier and screening_identifier:
            preg_women_obj = self.preg_women_cls.objects.filter(
                screening_identifier=screening_identifier)
            caregiver_child_consents = self.consent_cls.objects.filter(
                subject_consent__subject_identifier=subject_identifier, version='1')
            if preg_women_obj and caregiver_child_consents:
                for caregiver_child_consent in caregiver_child_consents:

                    caregiver_child_consents_dict = caregiver_child_consent.__dict__
                    exclude_options = ['consent_datetime', 'id', '_state',
                                       'created', 'modified', 'user_created',
                                       'user_modified']
                    for option in exclude_options:
                        del caregiver_child_consents_dict[option]
                    initial.append(caregiver_child_consents_dict)

        formset = super().get_formset(request, obj=obj, **kwargs)
        formset.form = self.auto_number(formset.form)
        formset.__init__ = partialmethod(formset.__init__, initial=initial)
        return formset

    def get_extra(self, request, obj=None, **kwargs):
        extra = super().get_extra(request, obj, **kwargs)
        study_maternal_id = request.GET.get('study_maternal_identifier')
        subject_identifier = request.GET.get('subject_identifier')

        if subject_identifier:
            caregiver_child_consents = self.consent_cls.objects.filter(
                subject_consent__subject_identifier=subject_identifier, version='1')
            if not obj:
                extra = caregiver_child_consents.count()

        if study_maternal_id:
            child_datasets = self.child_dataset_cls.objects.filter(
                study_maternal_identifier=study_maternal_id)
            if not obj:
                child_count = child_datasets.count()
                extra = child_count
            else:
                extra = len(self.get_difference(child_datasets, obj))
        return extra

    def get_difference(self, model_objs, obj=None):
        cc_ids = obj.caregiverchildconsent_set.values_list(
            'study_child_identifier', flat=True)
        return [x for x in model_objs if x.study_child_identifier not in cc_ids]


@admin.register(SubjectConsent, site=flourish_caregiver_admin)
class SubjectConsentAdmin(ModelAdminBasicMixin, ModelAdminMixin,
                          SimpleHistoryAdmin, admin.ModelAdmin):
    form = SubjectConsentForm
    inlines = [CaregiverChildConsentInline, ]

    fieldsets = (
        (None, {
            'fields': (
                'biological_caregiver',
                'screening_identifier',
                'subject_identifier',
                'first_name',
                'last_name',
                'initials',
                'language',
                'recruit_source',
                'recruit_source_other',
                'recruitment_clinic',
                'recruitment_clinic_other',
                'is_literate',
                'witness_name',
                'dob',
                'is_dob_estimated',
                'citizen',
                'gender',
                'identity',
                'identity_type',
                'confirm_identity',
                'remain_in_study',
                'hiv_testing',
                'breastfeed_intent',
                'child_consent')}),
        ('Review Questions', {
            'fields': (
                'consent_reviewed',
                'study_questions',
                'assessment_score',
                'consent_signature',
                'consent_copy',
                'future_contact',
                'consent_datetime'),
            'description': 'The following questions are directed to the interviewer.'}),
        audit_fieldset_tuple)

    radio_fields = {
        'gender': admin.VERTICAL,
        'assessment_score': admin.VERTICAL,
        'citizen': admin.VERTICAL,
        'consent_copy': admin.VERTICAL,
        'consent_reviewed': admin.VERTICAL,
        'consent_signature': admin.VERTICAL,
        'is_dob_estimated': admin.VERTICAL,
        'identity_type': admin.VERTICAL,
        'is_literate': admin.VERTICAL,
        'language': admin.VERTICAL,
        'recruit_source': admin.VERTICAL,
        'recruitment_clinic': admin.VERTICAL,
        'study_questions': admin.VERTICAL,
        'remain_in_study': admin.VERTICAL,
        'hiv_testing': admin.VERTICAL,
        'breastfeed_intent': admin.VERTICAL,
        'future_contact': admin.VERTICAL,
        'biological_caregiver': admin.VERTICAL,
        'child_consent': admin.VERTICAL}

    list_display = ('subject_identifier',
                    'verified_by',
                    'is_verified',
                    'is_verified_datetime',
                    'first_name',
                    'initials',
                    'gender',
                    'dob',
                    'consent_datetime',
                    'recruit_source',
                    'recruitment_clinic',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')

    list_filter = ('language',
                   'is_verified',
                   'is_literate',
                   'identity_type')

    search_fields = ('subject_identifier', 'dob',)

    def get_actions(self, request):

        super_actions = super().get_actions(request)

        if ('flourish_caregiver.change_subjectconsent'
                in request.user.get_group_permissions()):
            consent_actions = [
                flag_as_verified_against_paper,
                unflag_as_verified_against_paper]

            # Add actions from this ModelAdmin.
            actions = (self.get_action(action) for action in consent_actions)
            # get_action might have returned None, so filter any of those out.
            actions = filter(None, actions)

            actions = self._filter_actions_by_permissions(request, actions)
            # Convert the actions into an OrderedDict keyed by name.
            actions = OrderedDict(
                (name, (func, name, desc))
                for func, name, desc in actions
            )

            super_actions.update(actions)

        return super_actions

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj) + ('biological_caregiver',)
        return (fields + audit_fields)

    def response_add(self, request, obj, **kwargs):
        response = self._redirector(obj)
        return response if response else super(
            SubjectConsentAdmin, self).response_add(request, obj)

    def response_change(self, request, obj):
        response = self._redirector(obj)
        return response if response else super(
            SubjectConsentAdmin, self).response_change(request, obj)

    def _redirector(self, obj):
        caregiver_locator = ScreeningPregWomen.objects.filter(
            screening_identifier=obj.screening_identifier)
        if caregiver_locator:
            return redirect(settings.DASHBOARD_URL_NAMES.get(
                'maternal_screening_listboard_url'))


@admin.register(CaregiverChildConsent, site=flourish_caregiver_admin)
class CaregiverChildConsentAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = CaregiverChildConsentForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_consent',
                'subject_identifier',
                'first_name',
                'last_name',
                'gender',
                'child_dob',
                'child_test',
                'child_remain_in_study',
                'child_preg_test',
                'child_knows_status',
                'identity',
                'identity_type',
                'confirm_identity',
                'consent_datetime']}

         ),
        audit_fieldset_tuple)

    radio_fields = {'gender': admin.VERTICAL,
                    'child_test': admin.VERTICAL,
                    'child_remain_in_study': admin.VERTICAL,
                    'child_preg_test': admin.VERTICAL,
                    'child_knows_status': admin.VERTICAL,
                    'identity_type': admin.VERTICAL}

    list_display = ('subject_identifier',
                    'verified_by',
                    'is_verified',
                    'is_verified_datetime',
                    'first_name',
                    'last_name',
                    'gender',
                    'child_dob',
                    'consent_datetime',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')

    list_filter = ('is_verified',
                   'gender',
                   'child_remain_in_study',
                   'child_knows_status',
                   'child_preg_test',
                   'identity_type')

    search_fields = ['subject_identifier', 'subject_consent__subject_identifier', ]

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['subject_consent'].queryset = \
            SubjectConsent.objects.filter(id=request.GET.get('subject_consent'))
        return super(CaregiverChildConsentAdmin, self).render_change_form(
            request, context, *args, **kwargs)

    def export_as_csv(self, request, queryset):
        queryset = queryset.defer('site_id', 'initials', 'dob',
                                  'is_dob_estimated', 'guardian_name',
                                  'subject_type', 'consent_reviewed',
                                  'study_questions', 'assessment_score',
                                  'consent_signature', 'consent_copy')

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % (
            self.get_export_filename())

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        ws = wb.add_sheet('%s')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = 'YYYY/MM/DD h:mm:ss'

        field_names = queryset[0].__dict__
        field_names = [a for a in field_names.keys()]
        field_names.remove('_state')

        field_names.append('protocol')
        field_names.append('study_maternal_identifier')

        for col_num in range(len(field_names)):
            ws.write(row_num, col_num, field_names[col_num], font_style)

        for obj in queryset:
            obj_data = obj.__dict__
            maternal_dataset_qs = self.related_maternal_dataset(
                identifier=obj_data['study_child_identifier'])
            extra_data = {}
            if maternal_dataset_qs:
                extra_data = maternal_dataset_qs.__dict__
            data = [obj_data[field] if field not in ['protocol', 'study_maternal_identifier']
                    else extra_data.get(field, '') for field in field_names]

            row_num += 1
            for col_num in range(len(data)):
                if isinstance(data[col_num], uuid.UUID):
                    ws.write(row_num, col_num, str(data[col_num]))
                elif isinstance(data[col_num], datetime.datetime):
                    data[col_num] = timezone.make_naive(data[col_num])
                    ws.write(row_num, col_num, data[col_num], xlwt.easyxf(
                        num_format_str='YYYY/MM/DD h:mm:ss'))
                elif isinstance(data[col_num], datetime.date):
                    ws.write(row_num, col_num, data[col_num], xlwt.easyxf(
                        num_format_str='YYYY/MM/DD'))
                else:
                    ws.write(row_num, col_num, data[col_num])
        wb.save(response)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')
    actions = [export_as_csv]

    def get_actions(self, request):

        super_actions = super().get_actions(request)

        if ('flourish_caregiver.change_caregiverchildconsent'
                in request.user.get_group_permissions()):
            consent_actions = [
                flag_as_verified_against_paper,
                unflag_as_verified_against_paper]

            # Add actions from this ModelAdmin.
            actions = (self.get_action(action) for action in consent_actions)
            # get_action might have returned None, so filter any of those out.
            actions = filter(None, actions)

            actions = self._filter_actions_by_permissions(request, actions)
            # Convert the actions into an OrderedDict keyed by name.
            actions = OrderedDict(
                (name, (func, name, desc))
                for func, name, desc in actions
            )

            super_actions.update(actions)

        return super_actions

    def previous_study_dataset(self, identifier=None):
        childdataset_cls = django_apps.get_model('flourish_child.childdataset')
        try:
            dataset_obj = childdataset_cls.objects.get(
                study_child_identifier=identifier)
        except childdataset_cls.DoesNotExist:
            return None
        else:
            return dataset_obj

    def related_maternal_dataset(self, identifier=None):
        maternaldataset_cls = django_apps.get_model(
            'flourish_caregiver.maternaldataset')
        childdataset = self.previous_study_dataset(identifier=identifier)
        if childdataset:
            maternal_identifier = childdataset.study_maternal_identifier
            try:
                dataset_obj = maternaldataset_cls.objects.only(
                    'study_maternal_identifier', 'protocol').get(
                    study_maternal_identifier=maternal_identifier)
            except maternaldataset_cls.DoesNotExist:
                return None
            else:
                return dataset_obj
        return None
