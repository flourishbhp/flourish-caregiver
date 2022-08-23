from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple
from django.apps import apps as django_apps

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

    extra_context_models = ['maternalarvduringpreg']

    def add_view(self, request, form_url='', extra_context=None):

        extra_context = extra_context or {}
        subject_identifier = request.GET.get('subject_identifier')
        if self.extra_context_models:
            extra_context = self.get_model_data_per_visit(
                subject_identifier=subject_identifier)
        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}
        subject_identifier = request.GET.get('subject_identifier')
        if self.extra_context_models:
            extra_context = self.get_model_data_per_visit(
                subject_identifier=subject_identifier)
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

    def get_model_data_per_visit(self, subject_identifier=None):
        model_dict = {}
        for model_name in self.extra_context_models:
            data_dict = {}
            model_cls = django_apps.get_model(f'flourish_caregiver.{model_name}')
            model_objs = model_cls.objects.filter(
                maternal_visit__subject_identifier=subject_identifier)
            for obj in model_objs:
                inlines = obj.maternalarvtableduringpreg_set.all()
                for inline_obj in inlines:
                    visit_code = obj.maternal_visit.visit_code
                    data_dict.setdefault(visit_code, [])
                    data_dict[visit_code].append(inline_obj)

            model_dict.update({model_name: data_dict})

        return model_dict


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
        'maternal_arv_at_delivery__maternal_visit__appointment__subject_identifier',
        'maternal_arv_at_delivery__maternal_visit__appointment__initials', ]

    radio_fields = {
        'arv_code': admin.VERTICAL,
    }
