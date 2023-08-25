from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_fieldsets.fieldlist import Remove
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverClinicalMeasurementsForm
from ..models import CaregiverClinicalMeasurements


@admin.register(CaregiverClinicalMeasurements, site=flourish_caregiver_admin)
class CaregiverClinicalMeasurementsAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = CaregiverClinicalMeasurementsForm

    list_display = ('maternal_visit', 'weight_kg', 'height',
                    'systolic_bp', 'diastolic_bp', 'waist_circ', 'hip_circ')

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'height',
                'weight_kg',
                'systolic_bp',
                'diastolic_bp',
                'confirm_values',
                'waist_circ',
                'hip_circ',
                'all_measurements',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'confirm_values': admin.VERTICAL,
        'all_measurements': admin.VERTICAL}

    conditional_fieldlists = {
        'a_antenatal1_schedule1': Remove('waist_circ', 'hip_circ'),
        'a_birth1_schedule1': Remove('height', 'waist_circ', 'hip_circ'),
        'tb_2_months_schedule': Remove('height', 'waist_circ', 'hip_circ'),
        'a_fu1_schedule1': Remove('height'),
        'a_fu2_schedule1': Remove('height'),
        'a_fu3_schedule1': Remove('height'),
        'b_fu1_schedule1': Remove('height'),
        'b_fu2_schedule1': Remove('height'),
        'b_fu3_schedule1': Remove('height'),
        'c_fu1_schedule1': Remove('height'),
        'c_fu2_schedule1': Remove('height'),
        'c_fu3_schedule1': Remove('height'),
    }

    def get_key(self, request, obj=None):
        super().get_key(request, obj)
        try:
            model_obj = self.get_instance(request)
        except ObjectDoesNotExist:
            return None
        else:
            if model_obj:
                return model_obj.schedule_name
