from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import TbRoutineHealthScreenForm
from ..models import TbRoutineHealthScreen
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(TbRoutineHealthScreen, site=flourish_caregiver_admin)
class TbRoutineHealthScreenAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TbRoutineHealthScreenForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'tb_screened',
                'screen_location',
                'screen_location_other',
                'pos_screen',
                'diagnostic_referral',
                'referral_reason'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'tb_screened': admin.VERTICAL,
                    'screen_location': admin.VERTICAL,
                    'pos_screen': admin.VERTICAL,
                    'diagnostic_referral': admin.VERTICAL}
