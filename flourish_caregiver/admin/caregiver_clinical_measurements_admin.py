from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverClinicalMeasurementsForm
from ..models import CaregiverClinicalMeasurements
from .modeladmin_mixins import CrfModelAdminMixin


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
                'is_preg',
                'waist_circ',
                'hip_circ'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'is_preg': admin.VERTICAL, }
