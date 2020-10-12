from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import flourish_maternal_admin
from ..forms import HivViralLoadCd4Form
from ..models import HivViralLoadAndCd4


@admin.register(HivViralLoadAndCd4, site=flourish_maternal_admin)
class HivViralLoadCd4Admin(ModelAdminMixin, admin.ModelAdmin):

    form = HivViralLoadCd4Form

    fieldsets = (
        (None, {
            'fields': [
                'last_cd4_count_known',
                'cd4_count',
                'cd4_count_date',
                'last_vl_known',
                'vl_detectable',
                'recent_vl_results',
                'hiv_results_quantifier',
                'last_vl_date'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'last_cd4_count_known': admin.VERTICAL,
        'last_vl_known': admin.VERTICAL,
        'vl_detectable': admin.VERTICAL,
        'hiv_results_quantifier': admin.VERTICAL, }
