from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverClinicalMeasurementsForm
from ..models import CaregiverClinicalMeasurements
from .modeladmin_mixins import CrfModelAdminMixin
from edc_fieldsets.fieldlist import Remove


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
                'weight_available',
                'weight_kg',
                'systolic_bp',
                'diastolic_bp',
                'confirm_values',
                'is_preg',
                'waist_circ',
                'hip_circ',
                'all_measurements',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'weight_available': admin.VERTICAL,
        'is_preg': admin.VERTICAL,
        'confirm_values': admin.VERTICAL, }

    conditional_fieldlists = {
        'a_birth1_schedule1': Remove('height'),
        'tb_2_months_schedule': Remove('height', 'is_preg', 'waist_circ', 'hip_circ'),

    }

    def get_key(self, request, obj=None):
        super().get_key(request, obj)
        try:
            model_obj = self.get_instance(request)
        except ObjectDoesNotExist:
            schedule_name = None
        else:
            if model_obj:
                return model_obj.schedule_name

