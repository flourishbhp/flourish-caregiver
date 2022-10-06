from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import TbReferralOutcomesForm
from ..models import TbReferralOutcomes
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(TbReferralOutcomes, site=flourish_caregiver_admin)
class TbReferralOutcomesAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TbReferralOutcomesForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'referral_clinic_appt',
                'further_tb_eval',
                'tb_diagnostic_perf',
                'tb_diagnose_pos',
                'tb_test_results',
                'tb_treat_start',
                'tb_prev_therapy_start',
                'tb_comments'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'referral_clinic_appt': admin.VERTICAL,
                    'further_tb_eval': admin.VERTICAL,
                    'tb_diagnostic_perf': admin.VERTICAL,
                    'tb_diagnose_pos': admin.VERTICAL,
                    'tb_treat_start': admin.VERTICAL,
                    'tb_prev_therapy_start': admin.VERTICAL, }
