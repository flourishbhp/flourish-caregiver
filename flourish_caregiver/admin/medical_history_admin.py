from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import MedicalHistoryForm
from ..models import MedicalHistory
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(MedicalHistory, site=flourish_caregiver_admin)
class MedicalHistoryAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MedicalHistoryForm

    list_display = ('maternal_visit', 'chronic_since',)
    list_filter = ('chronic_since',)

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'chronic_since',
                'caregiver_chronic',
                'caregiver_chronic_other',
                'who_diagnosis',
                'who',
                'who_other',
                'caregiver_medications',
                'caregiver_medications_other',
                'know_hiv_status',
                'current_illness',
                'current_symptoms',
                'current_symptoms_other',
                'symptoms_start_date',
                'clinic_visit',
                'comment']}
         ), audit_fieldset_tuple)

    radio_fields = {'chronic_since': admin.VERTICAL,
                    'who_diagnosis': admin.VERTICAL,
                    'know_hiv_status': admin.VERTICAL,
                    'current_illness': admin.VERTICAL,
                    'clinic_visit': admin.VERTICAL,
                    'med_history_changed': admin.VERTICAL}

    filter_horizontal = (
        'who', 'caregiver_chronic', 'caregiver_medications', 'current_symptoms')

    custom_form_labels = [
        FormLabel(
            field='med_history_changed',
            label=('Since the last scheduled visit in {previous}, has any of '
                   'your medical history changed?'),
            previous_appointment=True)
    ]

    @property
    def quarterly_schedules(self):
        schedules = self.cohort_schedules_cls.objects.filter(
            schedule_type__icontains='quarterly',
            onschedule_model__startswith='flourish_caregiver').values_list(
                'schedule_name', flat=True)
        return schedules

    @property
    def fu_schedules(self):
        schedules = self.cohort_schedules_cls.objects.filter(
            schedule_type__icontains='followup',
            onschedule_model__startswith='flourish_caregiver').exclude(
                schedule_type__icontains='quarterly').values_list(
                'schedule_name', flat=True)
        return schedules

    @property
    def conditional_fieldlists(self):
        schedules = ['a_birth1_schedule1']
        schedules.extend(list(self.quarterly_schedules))
        schedules.extend(list(self.fu_schedules))

        conditional_fieldlists = {}
        for schedule in schedules:
            conditional_fieldlists.update(
                {schedule: Insert('med_history_changed', after='report_datetime')})
        return conditional_fieldlists

    def get_key(self, request, obj=None):
        return super().get_key(request, obj)

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
