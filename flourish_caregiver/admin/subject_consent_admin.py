from _collections import OrderedDict
from functools import partialmethod

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.db.models import OuterRef, Subquery
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from edc_consent.actions import (
    flag_as_verified_against_paper, unflag_as_verified_against_paper)
from edc_constants.constants import FEMALE, MALE
from edc_model_admin import audit_fields, audit_fieldset_tuple, \
    ModelAdminFormAutoNumberMixin
from edc_model_admin import ModelAdminBasicMixin
from edc_model_admin import StackedInlineMixin
from simple_history.admin import SimpleHistoryAdmin
from pre_flourish.helper_classes.utils import is_flourish_eligible
from flourish_child.helper_classes.utils import child_utils

from .consent_amin_mixin import ConsentMixin
from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverChildConsentForm, SubjectConsentForm
from ..models import CaregiverChildConsent, CaregiverLocator, SubjectConsent


class CaregiverChildConsentInline(ConsentMixin, StackedInlineMixin,
                                  ModelAdminFormAutoNumberMixin, admin.StackedInline):
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
                'version',
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
    preg_women_cls = django_apps.get_model(
        'flourish_caregiver.screeningpregwomen')
    consent_cls = django_apps.get_model(
        'flourish_caregiver.caregiverchildconsent')
    caregiver_consent_cls = django_apps.get_model(
        'flourish_caregiver.subjectconsent')

    def save_model(self, request, obj, form, change):
        super(CaregiverChildConsentInline, self).save_model(
            request, obj, form, change)

    def get_formset(self, request, obj=None, **kwargs):
        study_maternal_id = request.GET.get('study_maternal_identifier')
        subject_identifier = None

        if request.GET.get('subject_identifier'):
            subject_identifier = request.GET.get('subject_identifier')
        else:
            screening_identifier = request.GET.get('screening_identifier')
            subject_identifier = self.get_subject_identifier(screening_identifier)

        if subject_identifier:
            initial = self.prepare_initial_values_based_on_subject(
                obj, subject_identifier)
        elif study_maternal_id:
            initial = self.prepare_initial_values_based_on_study(
                obj, study_maternal_id)
        else:
            initial = []

        initial = self.filter_for_unique_identifiers(initial)

        formset = super().get_formset(request, obj=obj, **kwargs)
        formset.form = self.auto_number(formset.form)
        formset.__init__ = partialmethod(formset.__init__, initial=initial)
        return formset

    def filter_for_unique_identifiers(self, lst):
        if not lst:
            return lst

        unique_subject_identifiers = list(
            {v.get('subject_identifier', v.get('study_child_identifier')): v for v in lst
             if 'subject_identifier' in v or 'study_child_identifier' in v}.values())

        return unique_subject_identifiers

    def prepare_initial_values_based_on_subject(self, obj, subject_identifier):
        return [self.prepare_subject_consent(consent) for consent in
                self.consents_filtered_by_subject(obj, subject_identifier)]

    def consents_filtered_by_subject(self, obj, subject_identifier):
        consents = self.consent_cls.objects.filter(
            subject_consent__subject_identifier=subject_identifier).order_by(
            'consent_datetime')

        if obj:
            consents = consents.filter(
                subject_consent__version=getattr(obj, 'version', None))
            subquery = consents.filter(
                subject_identifier=OuterRef('subject_identifier')).order_by(
                '-version').values('version')[:1]
            consents = consents.filter(version=Subquery(subquery))
            consents = set([c.subject_identifier for c in self.get_difference(
                consents, obj)])

        return consents

    def prepare_initial_values_based_on_study(self, obj, study_maternal_id):
        initial = []
        child_datasets = self.child_dataset_cls.objects.filter(
            study_maternal_identifier=study_maternal_id).order_by('study_child_identifier')

        if obj:
            child_datasets = self.get_difference(child_datasets, obj)

        for child in child_datasets:
            child_dict = self.prepare_child_dict(
                obj, child)
            initial.append(child_dict)

        return initial

    def prepare_child_dict(self, obj, child):
        child_dict = {
            'study_child_identifier': child.study_child_identifier,
            'gender': {'Male': MALE, 'Female': FEMALE}.get(child.infant_sex),
            'child_dob': child.dob
        }

        pre_flourish_child_consent_model_obj = (
            self.pre_flourish_child_consent_model_obj(
                study_child_identifier=child.study_child_identifier))

        if pre_flourish_child_consent_model_obj:
            exclude_options = ['consent_datetime', 'id', '_state',
                               'created', 'modified', 'user_created',
                               'user_modified', 'version', 'hostname_modified',
                               'hostname_created', 'revision', 'device_created',
                               'device_modified', 'site_id',
                               'subject_consent_id', 'subject_identifier',
                               'ineligibility', 'is_eligible',
                               'caregiver_visit_count', 'child_age_at_enrollment',
                               'verified_by', 'is_verified_datetime',
                               'is_verified']
            pre_flourish_child_consent_model_obj = (
                self.remove_dict_options(
                    pre_flourish_child_consent_model_obj.__dict__,
                    exclude_options))
            child_dict.update(pre_flourish_child_consent_model_obj)

        return child_dict

    def get_extra(self, request, obj=None, **kwargs):

        extra = (super().get_extra(request, obj, **kwargs) +
                 self.get_child_reconsent_extra(request))
        study_maternal_id = request.GET.get('study_maternal_identifier')
        subject_identifier = request.GET.get('subject_identifier')

        if subject_identifier:
            caregiver_child_consents = set(list(self.consent_cls.objects.filter(
                subject_consent__subject_identifier=subject_identifier
            ).values_list('subject_identifier', flat=True)))

            if not obj:
                extra = len(caregiver_child_consents)

        elif study_maternal_id:
            child_datasets = self.get_child_datasets(study_maternal_id)
            if not obj:
                child_count = child_datasets.count()
                extra = child_count
            else:
                extra = len(self.get_difference(child_datasets, obj))
        return extra

    def get_child_datasets(self, study_maternal_identifier):
        """ Returns child dataset instances for specific maternal identifier
            if participant is not from Pre-flourish otherwise check eligibility
            first.
        """
        maternaldataset_cls = django_apps.get_model(
            'flourish_caregiver.maternaldataset')
        maternaldataset_exists = maternaldataset_cls.objects.filter(
            study_maternal_identifier=study_maternal_identifier,
            protocol='BCPP').exists()
        eligible_idxs = []

        child_datasets = self.child_dataset_cls.objects.filter(
                study_maternal_identifier=study_maternal_identifier)

        for child_dataset in child_datasets:
            is_eligible, _ = is_flourish_eligible(child_dataset.study_child_identifier)
            if is_eligible:
                eligible_idxs.append(child_dataset.study_child_identifier)

        if maternaldataset_exists:
            child_datasets = child_datasets.filter(study_child_identifier__in=eligible_idxs)

        return child_datasets

    def get_child_reconsent_extra(self, request):
        screening_identifier = request.GET.get('screening_identifier')
        subject_identifier = request.GET.get('subject_identifier')

        consent_version_obj = self.consent_version_obj(screening_identifier)
        child_version = getattr(consent_version_obj, 'child_version', None)
        if consent_version_obj and child_version:
            child_consent_objs = self.get_caregiver_child_consents(subject_identifier, )
            child_consents_by_version = self.get_caregiver_child_consents(
                subject_identifier, child_version)

            return len(child_consent_objs - child_consents_by_version)
        return 0

    pre_flourish_child_consent_model = 'pre_flourish.preflourishcaregiverchildconsent'

    @property
    def pre_flourish_child_consent_cls(self):
        return django_apps.get_model(self.pre_flourish_child_consent_model)

    def pre_flourish_child_consent_model_obj(self, study_child_identifier):
        try:
            return self.pre_flourish_child_consent_cls.objects.get(
                subject_identifier=study_child_identifier)
        except self.pre_flourish_child_consent_cls.DoesNotExist:
            return None

    def get_subject_identifier(self, screening_identifier):
        try:
            return self.caregiver_consent_cls.objects.filter(
                screening_identifier=screening_identifier).latest(
                'consent_datetime').subject_identifier
        except self.caregiver_consent_cls.DoesNotExist:
            return None


@admin.register(SubjectConsent, site=flourish_caregiver_admin)
class SubjectConsentAdmin(ConsentMixin, ModelAdminBasicMixin, ModelAdminMixin,
                          SimpleHistoryAdmin, admin.ModelAdmin):
    form = SubjectConsentForm
    inlines = [CaregiverChildConsentInline, ]

    consent_cls = django_apps.get_model(
        'flourish_caregiver.subjectconsent')

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

    def export_linkage_csv(self, request, queryset):
        records = []
        _existing = []
        for obj in queryset:
            study_maternal_identifier = self.study_maternal_identifier(
                screening_identifier=obj.screening_identifier)
            caregiver_data = dict(
                matpid=obj.subject_identifier,
                old_matpid=study_maternal_identifier, )

            child_consents = obj.caregiverchildconsent_set.values(
                'subject_identifier', 'study_child_identifier')
            for child_consent in child_consents:
                data = {}
                subject_identifier = child_consent.get('subject_identifier')
                study_child_identifier = child_consent.get('study_child_identifier')
                maternal_dataset = self.related_maternal_dataset(
                    study_child_identifier)
                enrol_cohort, curr_cohort = self.get_cohort_details(subject_identifier)
                if subject_identifier not in _existing:
                    data.update(
                        **caregiver_data,
                        childpid=subject_identifier,
                        old_childpid=study_child_identifier,
                        previous_study=getattr(maternal_dataset, 'protocol', None),
                        enrol_cohort=enrol_cohort,
                        current_cohort=curr_cohort)
                    records.append(data)
                    _existing.append(subject_identifier)
        _model = self.model
        self.model = None
        response = self.write_to_csv(
            records, app_label='CaregiverChildLinkage', export_type='csv')
        self.model = _model
        return response

    export_linkage_csv.short_description = _(
        'Export linkage CSV')

    actions = [export_linkage_csv]

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
        caregiver_locator = CaregiverLocator.objects.filter(
            screening_identifier=obj.screening_identifier)
        kwargs = {'subject_identifier': obj.subject_identifier}
        if caregiver_locator.count() > 0:
            return redirect(settings.DASHBOARD_URL_NAMES.get(
                'subject_dashboard_url'), **kwargs)
        else:
            return redirect(settings.DASHBOARD_URL_NAMES.get(
                'maternal_screening_listboard_url'))

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        subject_identifier = None
        initial_values = []
        if request.method == 'GET':
            study_maternal_identifier = request.GET.get('study_maternal_identifier')
            screening_identifier = request.GET.get('screening_identifier')

            if request.GET.get('subject_identifier'):
                subject_identifier = request.GET.get('subject_identifier')
            else:
                subject_identifier = self.get_subject_identifier(screening_identifier)
            if subject_identifier:
                initial_values = self.prepare_initial_values_based_on_subject(
                    subject_identifier=subject_identifier)
            elif study_maternal_identifier:
                initial_values = self.prepare_initial_values_from_locator(
                    study_maternal_identifier, screening_identifier)

        form.previous_instance = initial_values
        return form

    def prepare_initial_values_based_on_subject(self, subject_identifier):
        return [self.prepare_subject_consent(subject_identifier)]

    def prepare_initial_values_from_locator(
            self, study_maternal_identifier, screening_identifier):
        bhp_prior_screening_model_obj = self.bhp_prior_screening_model_obj(
            screening_identifier)
        locator_model_obj = self.locator_model_obj(study_maternal_identifier)
        pre_flourish_consent_model_obj = self.pre_flourish_consent_model_obj(
            screening_identifier)

        return [self.generate_participant_options(
            bhp_prior_screening_model_obj=bhp_prior_screening_model_obj,
            locator_model_obj=locator_model_obj,
            pre_flourish_consent_model_obj=pre_flourish_consent_model_obj
        )]


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
                'version',
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

    search_fields = ['subject_identifier',
                     'subject_consent__subject_identifier', ]

    def render_change_form(self, request, context, *args, **kwargs):
        if self.has_change_permission(request):
            context['adminform'].form.fields['subject_consent'].queryset = \
                SubjectConsent.objects.filter(
                    id=request.GET.get('subject_consent'))
        return super(CaregiverChildConsentAdmin, self).render_change_form(
            request, context, *args, **kwargs)

    def export_as_csv(self, request, queryset):
        queryset = queryset.defer('site_id', 'initials', 'dob', 'id',
                                  'is_dob_estimated', 'guardian_name',
                                  'subject_type', 'consent_reviewed',
                                  'study_questions', 'assessment_score',
                                  'consent_signature', 'consent_copy',
                                  'first_name', 'last_name', 'identity',
                                  'confirm_identity', 'subject_consent_id')

        records = []
        for obj in queryset:
            obj_data = obj.__dict__

            parent_obj = getattr(obj, 'subject_consent', None)
            caregiver_sid = getattr(parent_obj, 'subject_identifier', None)

            maternal_dataset_qs = self.related_maternal_dataset(
                identifier=getattr(obj, 'study_child_identifier', caregiver_sid))
            extra_data = {}
            if maternal_dataset_qs:
                extra_data = maternal_dataset_qs.__dict__

            exposure_status = child_utils.child_hiv_exposure(
                obj.subject_identifier,
                obj.study_child_identifier,
                caregiver_sid)
            extra_data.update({'caregiver_subject_identifier': caregiver_sid})
            extra_data.update({'hiv_exposure': exposure_status})
            extra_data.update({'study_status': self.study_status(obj.subject_identifier)})

            # Update current and enrollment cohort
            enrol_cohort, current_cohort = self.get_cohort_details(obj.subject_identifier)
            consent_cohort = self.get_cohort_by_date(
                obj.subject_identifier, obj.consent_datetime)
            extra_data.update(enrol_cohort=enrol_cohort,
                              cohort=current_cohort,
                              consent_cohort=consent_cohort)

            obj_data.update(extra_data)

            # Update variable names for study identifiers
            obj_data = self.update_variables(obj_data)
            # Exclude identifying values
            obj_data = self.remove_exclude_fields(obj_data)
            # Correct date formats
            obj_data = self.fix_date_formats(obj_data)
            records.append(obj_data)

        response = self.write_to_csv(records)
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

    def get_cohort_by_date(self, subject_identifier, report_datetime):
        """ Query cohort instances to get cohort details for a particular date.
            i.e. cohort participant was enrolled on at a specificied date.
            @param subject_identifier: child subject_identifier
            @param report_datetime: datetime to query for
            @return: cohort name
        """
        try:
            child_cohort = self.cohort_model_cls.objects.filter(
                subject_identifier=subject_identifier,
                assign_datetime__date__lte=report_datetime.date()).latest(
                'assign_datetime')
        except self.cohort_model_cls.DoesNotExist:
            return ''
        else:
            return child_cohort.name

    def update_variables(self, data={}):
        """ Update study identifiers to desired variable name(s).
        """
        new_data_dict = {}
        replace_idx = {'subject_identifier': 'childpid',
                       'caregiver_subject_identifier': 'matpid',
                       'study_maternal_identifier': 'old_matpid',
                       'study_child_identifier': 'old_childpid'}
        for old_idx, new_idx in replace_idx.items():
            try:
                new_data_dict[new_idx] = data.pop(old_idx)
            except KeyError:
                continue
        new_data_dict.update(data)
        return new_data_dict

    def study_status(self, subject_identifier=None):
        if not subject_identifier:
            return ''
        child_offstudy_cls = django_apps.get_model(
            'flourish_prn.childoffstudy')
        is_offstudy = child_offstudy_cls.objects.filter(
            subject_identifier=subject_identifier).exists()

        return 'off_study' if is_offstudy else 'on_study'
