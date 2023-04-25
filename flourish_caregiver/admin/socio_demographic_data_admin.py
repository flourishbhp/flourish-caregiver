from functools import partialmethod
from django.apps import apps as django_apps
from django.contrib import admin
from edc_fieldsets.fieldlist import Fieldlist
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import StackedInlineMixin, ModelAdminFormAutoNumberMixin, audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import SocioDemographicDataForm, HouseHoldDetailsForm
from ..models import SocioDemographicData, HouseHoldDetails, SubjectConsent, MaternalVisit
from .modeladmin_mixins import CrfModelAdminMixin
from edc_fieldsets import Fieldsets


class HouseHoldDetailsInlineAdmin(StackedInlineMixin, ModelAdminFormAutoNumberMixin, admin.StackedInline):
    model = HouseHoldDetails
    form = HouseHoldDetailsForm
    extra = 0
    max_num = 0

    fieldsets = (
        (None, {
            'fields': (
                'child_identifier',
                'stay_with_child', )
            }),
        )

    radio_fields = {'stay_with_child': admin.VERTICAL}

    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        formset = super().get_formset(request, obj, **kwargs)
        twin_enrol = self.twin_enrolment(request.GET.get('subject_identifier', ''))
        for sidx in twin_enrol:
            initial.append({'child_identifier': sidx})
        formset.__init__ = partialmethod(formset.__init__, initial=initial)
        formset.form = self.auto_number(formset.form)
        return formset

    def get_extra(self, request, obj=None, **kwargs):
        extra = super().get_extra(request, obj, **kwargs)

        subject_identifier = request.GET.get('subject_identifier', '')
        maternal_visit = request.GET.get('maternal_visit', '')

        twin_enrol = self.twin_enrolment(subject_identifier)

        child_sidx = self.onschedule_sid(obj, maternal_visit_id=maternal_visit)
        if child_sidx and child_sidx in twin_enrol:
            return len(twin_enrol)
        return extra

    def get_max_num(self, request, obj=None, **kwargs):
        max_num = super().get_max_num(request, obj=obj, **kwargs)

        subject_identifier = request.GET.get('subject_identifier', '')
        maternal_visit = request.GET.get('maternal_visit', '')

        twin_enrol = self.twin_enrolment(subject_identifier)

        child_sidx = self.onschedule_sid(obj, maternal_visit_id=maternal_visit)
        if child_sidx and child_sidx in twin_enrol:
            return len(twin_enrol)
        return max_num

    def onschedule_sid(self, obj, maternal_visit_id=None):
        maternal_visit = getattr(obj, 'maternal_visit', None)
        if not maternal_visit and maternal_visit_id:
            maternal_visit = MaternalVisit.objects.get(pk=maternal_visit_id)

        if not maternal_visit:
            return None

        onschedule_cls = django_apps.get_model(
            maternal_visit.appointment.schedule.onschedule_model)
        subject_identifier = maternal_visit.subject_identifier

        try:
            on_schedule_obj = onschedule_cls.objects.get(
                subject_identifier=subject_identifier,
                schedule_name=maternal_visit.schedule_name)
        except self.onschedule_cls.DoesNotExist:
            return None
        else:
            return on_schedule_obj.child_subject_identifier

    def subject_consents(self, subject_identifier=None):
        return SubjectConsent.objects.filter(subject_identifier=subject_identifier)

    def latest_consent(self, consents=None):
        try:
            return consents.latest('consent_datetime')
        except SubjectConsent.DoesNotExist:
            return None

    def twin_enrolment(self, subject_identifier=None):
        child_consents = []
        dataset_cls = django_apps.get_model('flourish_caregiver.maternaldataset')
        child_dataset_cls = django_apps.get_model('flourish_child.childdataset')

        consents = self.subject_consents(subject_identifier)
        latest_consent = self.latest_consent(consents)
        twin_enrol = getattr(latest_consent, 'multiple_birth', None)
        if not twin_enrol:
            return []

        try:
            dataset_obj = dataset_cls.objects.get(
                screening_identifier=getattr(latest_consent, 'screening_identifier', None))
        except dataset_cls.DoesNotExist:
            return []
        else:
            children = child_dataset_cls.objects.filter(
                study_maternal_identifier=dataset_obj.study_maternal_identifier).values_list(
                    'study_child_identifier', flat=True)

            for consent in consents:
                sidx = consent.caregiverchildconsent_set.filter(
                    study_child_identifier__in=list(children)).values_list('subject_identifier', flat=True)
                child_consents.extend(sidx)
            return list(set(child_consents))


@admin.register(SocioDemographicData, site=flourish_caregiver_admin)
class SocioDemographicDataAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = SocioDemographicDataForm
    inlines = [HouseHoldDetailsInlineAdmin, ]

    list_display = ('maternal_visit',
                    'marital_status',
                    'ethnicity',
                    'highest_education')
    list_filter = ('marital_status',
                   'ethnicity',
                   'highest_education')

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'marital_status',
                'marital_status_other',
                'ethnicity',
                'ethnicity_other',
                'highest_education',
                'current_occupation',
                'current_occupation_other',
                'provides_money',
                'provides_money_other',
                'money_earned',
                'money_earned_other',
                'stay_with_child',
                'number_of_household_members'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'marital_status': admin.VERTICAL,
                    'ethnicity': admin.VERTICAL,
                    'highest_education': admin.VERTICAL,
                    'current_occupation': admin.VERTICAL,
                    'provides_money': admin.VERTICAL,
                    'money_earned': admin.VERTICAL,
                    'stay_with_child': admin.VERTICAL,
                    'socio_demo_changed': admin.VERTICAL}

    conditional_fieldlists = {}

    custom_form_labels = [
        FormLabel(
            field='socio_demo_changed',
            label=('Since the last time you spoke to a FLOURISH study member, has any of your'
                   ' following Socio-demographic information changed'),
            previous_appointment=True)
    ]

    quartely_schedules = ['a_quarterly1_schedule1', 'a_quarterly2_schedule1',
                          'a_quarterly3_schedule1', 'a_sec_quart1_schedule1',
                          'a_sec_quart2_schedule1', 'a_sec_quart3_schedule1',
                          'b_quarterly1_schedule1', 'b_quarterly2_schedule1',
                          'b_quarterly3_schedule1', 'c_quarterly2_schedule1',
                          'c_quarterly1_schedule1', 'c_quarterly3_schedule1',
                          'b_sec_quart1_schedule1', 'b_sec_quart2_schedule1',
                          'b_sec_quart3_schedule1', 'c_sec_quart1_schedule1',
                          'c_sec_quart2_schedule1', 'c_sec_quart3_schedule1',
                          'pool1_schedule1', 'pool2_schedule1', 'pool3_schedule1']

    fu_schedules = ['a_fu1_schedule1', 'a_fu2_schedule1',
                    'a_fu3_schedule1',
                    'a_fu_quarterly1_schedule1', 'a_fu_quarterly2_schedule1',
                    'a_fu_quarterly3_schedule1',
                    'b_fu1_schedule1',
                    'b_fu2_schedule1', 'b_fu3_schedule1',
                    'b_fu_quarterly1_schedule1', 'b_fu_quarterly2_schedule1',
                    'b_fu_quarterly3_schedule1',
                    'c_fu1_schedule1',
                    'c_fu2_schedule1', 'c_fu3_schedule1',
                    'c_fu_quarterly1_schedule1', 'c_fu_quarterly2_schedule1',
                    'c_fu_quarterly3_schedule1']

    schedules = quartely_schedules + fu_schedules

    for schedule in schedules:

        conditional_fieldlists.update(
            {schedule: Fieldlist(insert_fields=('socio_demo_changed',),
                                 remove_fields=('number_of_household_members',),
                                 insert_after='report_datetime')})

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)

        inlines = self.get_inline_instances(request, obj)

        household_instance = inlines[0]

        subject_identifier = request.GET.get('subject_identifier', '')

        twin_enrol = household_instance.twin_enrolment(subject_identifier)
        maternal_visit = request.GET.get('maternal_visit', '')

        child_sidx = household_instance.onschedule_sid(obj, maternal_visit_id=maternal_visit)

        if child_sidx and child_sidx in twin_enrol:
            fieldsets = Fieldsets(fieldsets=fieldsets)
            try:
                fieldsets.remove_fields(
                    *('stay_with_child', ),
                    section=None)
            except AttributeError:
                pass
            else:
                return fieldsets.fieldsets
        return fieldsets
