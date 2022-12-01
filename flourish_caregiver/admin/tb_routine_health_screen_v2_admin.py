from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import TbRoutineHealthScreenV2Form
from ..models import TbRoutineHealthScreenV2
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(TbRoutineHealthScreenV2, site=flourish_caregiver_admin)
class TbRoutineHealthScreenVersionTwoAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TbRoutineHealthScreenV2Form

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'tb_health_visits',
                'tb_screened',
                'screen_location',
                'screen_location_other',
                'diagnostic_referral',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'tb_screened': admin.VERTICAL,
                    'tb_health_visits': admin.HORIZONTAL,
                    'diagnostic_referral': admin.VERTICAL,
                    }

    filter_horizontal = ('screen_location',)