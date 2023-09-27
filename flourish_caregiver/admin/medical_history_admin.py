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
                    'med_history_changed': admin.VERTICAL}

    filter_horizontal = (
        'who', 'caregiver_chronic', 'caregiver_medications')

    custom_form_labels = [
        FormLabel(
            field='med_history_changed',
            label=('Since the last scheduled visit in {previous}, has any of '
                   'your medical history changed?'),
            previous_appointment=True)
    ]

    schedule_names = ['a_quarterly1_schedule1', 'a_quarterly2_schedule1',
                      'a_quarterly3_schedule1', 'a_sec_quart1_schedule1',
                      'a_sec_quart2_schedule1', 'a_sec_quart3_schedule1',
                      'b_quarterly1_schedule1', 'b_quarterly2_schedule1',
                      'b_quarterly3_schedule1', 'c_quarterly2_schedule1',
                      'c_quarterly1_schedule1', 'c_quarterly3_schedule1',
                      'b_sec_quart1_schedule1', 'b_sec_quart2_schedule1',
                      'b_sec_quart3_schedule1', 'c_sec_quart1_schedule1',
                      'c_sec_quart2_schedule1', 'c_sec_quart3_schedule1',
                      'pool1_schedule1', 'pool2_schedule1', 'pool3_schedule1',
                      'a_birth1_schedule1', ]

    fu_schedule_names = ['a_fu1_schedule1', 'a_fu2_schedule1',
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

    schedules = schedule_names + fu_schedule_names

    conditional_fieldlists = {}
    for schedule in schedules:
        conditional_fieldlists.update(
            {schedule: Insert('med_history_changed', after='report_datetime')})

    def get_key(self, request, obj=None):
        return super().get_key(request, obj)

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
