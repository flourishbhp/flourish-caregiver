from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import TbStudyScreeningForm
from ..models import TbStudyEligibility
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(TbStudyEligibility, site=flourish_caregiver_admin)
class TbStudyEligibilityAdmin(CrfModelAdminMixin):
    form = TbStudyScreeningForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'tb_participation',
                'reasons_not_participating',
                'reasons_not_participating_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'tb_participation': admin.VERTICAL,
        'reasons_not_participating': admin.VERTICAL,
    }
