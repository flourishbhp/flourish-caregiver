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
                'tb_eval',
                'tb_eval_location',
                'tb_eval_location_other',
                'tb_eval_comments',
                'tb_diagnostic_perf',
                'tb_diagnostics',
                'tb_diagnostics_other',
                'tb_diagnose_pos',
                'tb_test_results',
                'tb_treat_start',
                'tb_prev_therapy_start',
                'tb_comments'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'tb_eval': admin.VERTICAL,
        'tb_eval_location': admin.VERTICAL,
        'tb_diagnostic_perf': admin.VERTICAL,
        'tb_diagnose_pos': admin.VERTICAL,
        'tb_treat_start': admin.VERTICAL,
        'tb_prev_therapy_start': admin.VERTICAL, }

    filter_horizontal = ('tb_diagnostics',)
