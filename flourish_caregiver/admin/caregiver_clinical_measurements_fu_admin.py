from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverClinicalMeasurementsFuForm
from ..models import CaregiverClinicalMeasurementsFu


@admin.register(CaregiverClinicalMeasurementsFu, site=flourish_caregiver_admin)
class CaregiverClinicalMeasurementsFuAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverClinicalMeasurementsFuForm

    list_display = ('maternal_visit', 'weight_kg', 'systolic_bp',
                    'waist_circ', 'hip_circ')

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'weight_kg',
                'systolic_bp',
                'waist_circ',
                'hip_circ'
            ]}
         ), audit_fieldset_tuple)
