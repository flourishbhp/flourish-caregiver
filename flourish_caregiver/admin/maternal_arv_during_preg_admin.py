from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalArvDuringPregForm, MaternalArvForm
from ..models import MaternalArvDuringPreg, MaternalArv
from .modeladmin_mixins import CrfModelAdminMixin, ModelAdminMixin


class MaternalArvInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = MaternalArv
    form = MaternalArvForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': [
                'arv_code',
                'start_date',
                'stop_date',
                'reason_for_stop',
                'reason_for_stop_other']}
         ), audit_fieldset_tuple)


@admin.register(MaternalArvDuringPreg, site=flourish_caregiver_admin)
class MaternalArvDuringPregAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = MaternalArvDuringPregForm
    inlines = [MaternalArvInlineAdmin, ]
    list_display = ('maternal_visit', 'took_arv', 'is_interrupt',)
    list_filter = ('took_arv',)

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'took_arv',
                'is_interrupt',
                'interrupt',
                'interrupt_other']}
         ),)

    radio_fields = {'took_arv': admin.VERTICAL,
                    'is_interrupt': admin.VERTICAL,
                    'interrupt': admin.VERTICAL
                    }


@admin.register(MaternalArv, site=flourish_caregiver_admin)
class MaternalArvAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = MaternalArvForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_arv_durg_preg',
                'arv_code',
                'start_date',
                'stop_date',
                'reason_for_stop',
                'reason_for_stop_other',
            ]
        }

        ), audit_fieldset_tuple,
    )
    list_display = ('arv_code', 'start_date', 'stop_date', 'reason_for_stop', )

    search_fields = [
        'maternal_arv_durg_preg__child_visit__appointment__subject_identifier',
        'maternal_arv_durg_preg__child_visit__appointment__initials', ]

    radio_fields = {
        'arv_code': admin.VERTICAL,
        'reason_for_stop': admin.VERTICAL
    }
