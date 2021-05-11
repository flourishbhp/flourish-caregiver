from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import MedicalHistoryForm
from ..models import MedicalHistory


@admin.register(MedicalHistory, site=flourish_caregiver_admin)
class MedicalHistoryAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MedicalHistoryForm

    list_display = ('maternal_visit', 'chronic_since', )
    list_filter = ('chronic_since', )

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
                'caregiver_medications',
                'caregiver_medications_other',
                'know_hiv_status',
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

    quartely_schedules = ['a_quarterly1_schedule1', 'a_quarterly2_schedule1',
                          'a_quarterly3_schedule1', 'a_sec1_schedule1',
                          'a_sec2_schedule1', 'a_sec3_schedule1',
                          'b_quarterly1_schedule1', 'b_quarterly2_schedule1',
                          'b_quarterly3_schedule1', 'c_quarterly2_schedule1',
                          'c_quarterly1_schedule1', 'c_quarterly3_schedule1',
                          'b_sec1_schedule1', 'b_sec2_schedule1', 'b_sec3_schedule1',
                          'c_sec1_schedule1', 'c_sec2_schedule1', 'c_sec3_schedule1',
                          'pool1_schedule1', 'pool2_schedule1', 'pool3_schedule1']

    conditional_fieldlists = {}
    for schedule in quartely_schedules:
        conditional_fieldlists.update(
            {schedule: Insert('med_history_changed', after='report_datetime')})
