from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverTBScreeningForm
from ..models import CaregiverTBScreening


@admin.register(CaregiverTBScreening, site=flourish_caregiver_admin)
class CaregiverTBScreeningAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = CaregiverTBScreeningForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'cough',
                'cough_duration',
                'fever',
                'fever_duration',
                'sweats',
                'sweats_duration',
                'weight_loss',
                'weight_loss_duration',
                'household_diagnosed_with_tb',
                'evaluated_for_tb',
                'clinic_visit_date',
                'tb_tests',
                'other_test',
                'chest_xray_results',
                'sputum_sample_results',
                'urine_test_results',
                'skin_test_results',
                'blood_test_results',
                'other_test_results',
                'diagnosed_with_TB',
                'diagnosed_with_TB_other',
                'started_on_TB_treatment',
                'started_on_TB_treatment_other',
                'started_on_TB_preventative_therapy',
                'started_on_TB_preventative_therapy_other',
            ]}),
        audit_fieldset_tuple
    )

    radio_fields = {
        "cough": admin.VERTICAL,
        "cough_duration": admin.VERTICAL,
        "fever": admin.VERTICAL,
        "fever_duration": admin.VERTICAL,
        "sweats": admin.VERTICAL,
        "sweats_duration": admin.VERTICAL,
        "weight_loss": admin.VERTICAL,
        "weight_loss_duration": admin.VERTICAL,
        "household_diagnosed_with_tb": admin.VERTICAL,
        "evaluated_for_tb": admin.VERTICAL,
        "chest_xray_results": admin.VERTICAL,
        "sputum_sample_results": admin.VERTICAL,
        "urine_test_results": admin.VERTICAL,
        "skin_test_results": admin.VERTICAL,
        "blood_test_results": admin.VERTICAL,
        "diagnosed_with_TB": admin.VERTICAL,
        "started_on_TB_treatment": admin.VERTICAL,
        "started_on_TB_preventative_therapy": admin.VERTICAL,
    }

    filter_horizontal = ('tb_tests',)
