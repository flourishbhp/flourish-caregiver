from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import HivViralLoadCd4Form
from ..models import HivViralLoadAndCd4


@admin.register(HivViralLoadAndCd4, site=flourish_caregiver_admin)
class HivViralLoadCd4Admin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HivViralLoadCd4Form

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'last_cd4_count_known',
                'cd4_count',
                'cd4_count_date',
                'last_vl_known',
                'vl_detectable',
                'hiv_results_quantifier',
                'recent_vl_results',
                'last_vl_date'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'last_cd4_count_known': admin.VERTICAL,
        'last_vl_known': admin.VERTICAL,
        'vl_detectable': admin.VERTICAL,
        'hiv_results_quantifier': admin.VERTICAL, }
