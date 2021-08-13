from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import TbHistoryPregForm
from ..models import TbHistoryPreg


@admin.register(TbHistoryPreg, site=flourish_caregiver_admin)
class TbHistoryPregAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TbHistoryPregForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'prior_tb_infec',
                'history_of_tbt',
                'tbt_completed',
                'prior_tb_history',
                'tb_diagnosis_type',
                'extra_pulmonary_loc',
                'prior_treatmnt_history',
                'tb_drugs_freq',
                'iv_meds_used',
                'tb_treatmnt_completed'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'prior_tb_infec': admin.VERTICAL,
                    'history_of_tbt': admin.VERTICAL,
                    'tbt_completed': admin.VERTICAL,
                    'prior_tb_history': admin.VERTICAL,
                    'tb_diagnosis_type': admin.VERTICAL,
                    'extra_pulmonary_loc': admin.VERTICAL,
                    'prior_treatmnt_history': admin.VERTICAL,
                    'tb_drugs_freq': admin.VERTICAL,
                    'iv_meds_used': admin.VERTICAL,
                    'tb_treatmnt_completed': admin.VERTICAL}
