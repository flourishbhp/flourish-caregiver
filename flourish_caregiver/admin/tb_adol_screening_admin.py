from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import TbAdolScreeningForm
from ..models import TbAdolEligibility
from .modeladmin_mixins import ModelAdminMixin


@admin.register(TbAdolEligibility, site=flourish_caregiver_admin)
class TbAdolEligibilityAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = TbAdolScreeningForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'tb_adol_participation',
                'reasons_unwilling_part',
                'reasons_unwilling_part_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'tb_adol_participation': admin.VERTICAL,
        'reasons_unwilling_part': admin.VERTICAL,
         }

    search_fields = ('subject_identifier',)
