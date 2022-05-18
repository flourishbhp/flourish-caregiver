from django.contrib import admin
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
                'weight_kg',
                'systolic_bp',
                'diastolic_bp',
                'confirm_values',
                'is_preg',
                'waist_circ',
                'hip_circ'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'is_preg': admin.VERTICAL, 
        'confirm_values': admin.VERTICAL, }

    conditional_fieldlists = {
        'a_birth1_schedule1': Remove('height'),
    }

    def get_key(self, request, obj=None):
        return super().get_key(request, obj)