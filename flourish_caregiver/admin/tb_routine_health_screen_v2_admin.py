from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_model_admin import audit_fieldset_tuple, StackedInlineMixin, ModelAdminFormAutoNumberMixin
from django.apps import apps as django_apps
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

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=obj, **kwargs)
        formset.form = self.auto_number(formset.form)
        return formset


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

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)

        custom_label = 'How many health visits have you had since you became pregnant?'
        model_obj = self.get_instance(request)
        if model_obj and model_obj.visit_code in ['1000M', '2000M']:
            form.base_fields['tb_health_visits'].label = custom_label
        form = self.auto_number(form)
        return form
