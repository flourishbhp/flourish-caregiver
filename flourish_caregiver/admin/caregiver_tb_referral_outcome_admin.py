from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from flourish_caregiver.admin.modeladmin_mixins import CrfModelAdminMixin
from flourish_caregiver.admin_site import flourish_caregiver_admin
from flourish_caregiver.forms.caregiver_tb_referral_outcome_form import \
    CaregiverTBReferralOutcomeForm
from flourish_caregiver.models.caregiver_tb_referral_outcome import \
    CaregiverTBReferralOutcome


@admin.register(CaregiverTBReferralOutcome, site=flourish_caregiver_admin)
class CaregiverTBReferralOutcomeAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = CaregiverTBReferralOutcomeForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'tb_evaluation',
                'clinic_name',
                'clinic_name_other',
                'evaluated',
                'reason_not_evaluated',
                'reason_not_evaluated_other',
                'tests_performed',
                'comments',
                'other_test_specify',
                'chest_xray_results',
                'sputum_sample_results',
                'urine_test_results',
                'skin_test_results',
                'blood_test_results',
                'other_test_results',
                'diagnosed_with_tb',
                'tb_treatment',
                'other_tb_treatment',
                'tb_preventative_therapy',
                'other_tb_preventative_therapy',
                'reasons',
                'other_reasons',
            ]}
         ), audit_fieldset_tuple)

    filter_horizontal = ('tests_performed',)

    radio_fields = {'tb_evaluation': admin.VERTICAL,
                    'clinic_name': admin.VERTICAL,
                    'evaluated':admin.VERTICAL,
                    'reason_not_evaluated':admin.VERTICAL,
                    'chest_xray_results': admin.VERTICAL,
                    'sputum_sample_results': admin.VERTICAL,
                    'urine_test_results': admin.VERTICAL,
                    'skin_test_results': admin.VERTICAL,
                    'blood_test_results': admin.VERTICAL,
                    'other_test_results': admin.VERTICAL,
                    'diagnosed_with_tb': admin.VERTICAL,
                    'tb_treatment': admin.VERTICAL,
                    'tb_preventative_therapy': admin.VERTICAL,
                    'reasons': admin.VERTICAL}
