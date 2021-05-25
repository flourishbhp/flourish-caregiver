from django.apps import apps as django_apps
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_consent.actions import (
    flag_as_verified_against_paper, unflag_as_verified_against_paper)
from edc_model_admin import (
    ModelAdminFormAutoNumberMixin, ModelAdminInstitutionMixin,
    audit_fieldset_tuple, audit_fields, ModelAdminNextUrlRedirectMixin,
    ModelAdminNextUrlRedirectError, ModelAdminReplaceLabelTextMixin)
from edc_model_admin import ModelAdminBasicMixin, ModelAdminReadOnlyMixin
from edc_model_admin import StackedInlineMixin
from functools import partialmethod
from simple_history.admin import SimpleHistoryAdmin

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverChildConsentForm, SubjectConsentForm
from ..models import CaregiverChildConsent, SubjectConsent
from .exportaction_mixin import ExportActionMixin
from _collections import OrderedDict
from edc_constants.constants import MALE, FEMALE


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin, ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin, ModelAdminReadOnlyMixin,
                      ExportActionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url


class CaregiverChildConsentInline(StackedInlineMixin, ModelAdminFormAutoNumberMixin,
                                  admin.StackedInline):

    model = CaregiverChildConsent
    form = CaregiverChildConsentForm

    extra = 1
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

    def get_max_num(self, request, obj=None, **kwargs):
        maternal_delivery = django_apps.get_model('flourish_caregiver.maternaldelivery')
        dummy_consent = django_apps.get_model('flourish_child.childdummysubjectconsent')

        if request.GET.get('antenatal') == 'True':
            if obj:
                self.max_num = dummy_consent.objects.filter(
                    subject_identifier__icontains=obj.subject_identifier).count()
                try:
                    maternal_delivery.objects.get(subject_identifier=obj.subject_identifier)
                except maternal_delivery.DoesNotExist:
                    pass
                else:
                    self.max_num += 1
            else:
                self.max_num = 0
        return super().get_max_num(request, obj=None, **kwargs)

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

        formset = super().get_formset(request, obj=obj, **kwargs)
        formset.form = self.auto_number(formset.form)
        formset.__init__ = partialmethod(formset.__init__, initial=initial)
        return formset

    def get_extra(self, request, obj=None, **kwargs):
        extra = super().get_extra(request, obj, **kwargs)
        study_maternal_id = request.GET.get('study_maternal_identifier')
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
         ),)

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
