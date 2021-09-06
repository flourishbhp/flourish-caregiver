from django.contrib import admin
from edc_fieldsets.fieldlist import Insert, Remove
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import audit_fieldset_tuple
from ..models import AntenatalEnrollment
from ..admin_site import flourish_caregiver_admin
from ..forms import SocioDemographicDataForm
from ..models import SocioDemographicData
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SocioDemographicData, site=flourish_caregiver_admin)
class SocioDemographicDataAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = SocioDemographicDataForm

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
                          'a_quarterly3_schedule1', 'a_sec1_schedule1',
                          'a_sec2_schedule1', 'a_sec3_schedule1',
                          'b_quarterly1_schedule1', 'b_quarterly2_schedule1',
                          'b_quarterly3_schedule1', 'c_quarterly2_schedule1',
                          'c_quarterly1_schedule1', 'c_quarterly3_schedule1',
                          'b_sec1_schedule1', 'b_sec2_schedule1', 'b_sec3_schedule1',
                          'c_sec1_schedule1', 'c_sec2_schedule1', 'c_sec3_schedule1',
                          'pool1_schedule1', 'pool2_schedule1', 'pool3_schedule1']

    for schedule in quartely_schedules:
        conditional_fieldlists.update(
            {schedule: Insert('socio_demo_changed', after='report_datetime')})

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
