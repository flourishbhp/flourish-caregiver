from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalArvAtDeliveryForm, MaternalArvTableAtDeliveryForm
from ..models import MaternalArvTableAtDelivery, MaternalArvAtDelivery
from .modeladmin_mixins import CrfModelAdminMixin, ModelAdminMixin


class MaternalArvTableAtDeliveryInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = MaternalArvTableAtDelivery
    form = MaternalArvTableAtDeliveryForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': [
                'arv_code',
                'start_date',
                'stop_date',
                'date_resumed']}
         ), audit_fieldset_tuple)


@admin.register(MaternalArvAtDelivery, site=flourish_caregiver_admin)
class MaternalArvAtDeliveryAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = MaternalArvAtDeliveryForm
    inlines = [MaternalArvTableAtDeliveryInlineAdmin, ]
    list_display = ('maternal_visit', 'last_visit_change',)

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'last_visit_change',
                'change_reason',
                'change_reason_other',
                'resume_treat']}
         ),)

    radio_fields = {'last_visit_change': admin.VERTICAL,
                    'change_reason': admin.VERTICAL,
                    'resume_treat': admin.VERTICAL
                    }


@admin.register(MaternalArvTableAtDelivery, site=flourish_caregiver_admin)
class MaternalArvTableAtDeliveryAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = MaternalArvTableAtDeliveryForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_arv_at_delivery',
                'arv_code',
                'start_date',
                'stop_date',
                'date_resumed'
            ]
        }

         ), audit_fieldset_tuple,
    )
    list_display = ('arv_code', 'start_date', 'stop_date',)

    search_fields = [
        'maternal_arv_at_delivery__child_visit__appointment__subject_identifier',
        'maternal_arv_at_delivery__child_visit__appointment__initials', ]

    radio_fields = {
        'arv_code': admin.VERTICAL,
    }
