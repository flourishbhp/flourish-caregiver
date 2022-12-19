from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple, StackedInlineMixin, ModelAdminFormAutoNumberMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import TbRoutineHealthScreenV2Form, TbRoutineHealthEncountersForm
from ..models import TbRoutineHealthScreenV2, TbRoutineHealthEncounters
from .modeladmin_mixins import CrfModelAdminMixin


class TbRoutineHealthScreenInline(StackedInlineMixin, ModelAdminFormAutoNumberMixin,
                                  admin.StackedInline):
    model = TbRoutineHealthEncounters
    form = TbRoutineHealthEncountersForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'screen_location',
                'screen_location_other',
                'tb_screened',
                'pos_screen',
                'diagnostic_referral',
            )
        }),
        audit_fieldset_tuple
    )
    radio_fields = {'tb_screened': admin.VERTICAL,
                    'diagnostic_referral': admin.VERTICAL,
                    'pos_screen': admin.VERTICAL,
                    }

    filter_horizontal = ('screen_location',)


@admin.register(TbRoutineHealthScreenV2, site=flourish_caregiver_admin)
class TbRoutineHealthScreenVersionTwoAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = TbRoutineHealthScreenV2Form
    inlines = [TbRoutineHealthScreenInline, ]
    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'tb_health_visits',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'tb_health_visits': admin.VERTICAL, }
