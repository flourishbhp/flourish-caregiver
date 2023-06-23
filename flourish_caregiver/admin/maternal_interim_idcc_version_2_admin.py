from django.contrib import admin
from django.http import request
from edc_model_admin import audit_fieldset_tuple
from flourish_caregiver.models.maternal_hiv_interim_hx import MaternalHivInterimHx

from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalInterimIdccFormVersion2
from ..models import MaternalInterimIdccVersion2
from .modeladmin_mixins import CrfModelAdminMixin
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel


@admin.register(MaternalInterimIdccVersion2, site=flourish_caregiver_admin)
class MaternalInterimIdccVersion2Admin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MaternalInterimIdccFormVersion2
    change_form_template = 'admin/flourish_caregiver/maternalinterimidcc/change_form.html'
    add_form_template = 'admin/flourish_caregiver/maternalinterimidcc/change_form.html'

    list_display = ('maternal_visit', 'report_datetime',
                    'recent_cd4', 'value_vl',)

    list_filter = (
        'info_since_lastvisit', 'recent_cd4_date',
        'value_vl_size', 'recent_vl_date')

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'info_since_lastvisit',
                'laboratory_information_available',
                'last_visit_result',
                'reason_cd4_not_availiable',
                'reason_cd4_not_availiable_other',
                'recent_cd4',
                'recent_cd4_date',
                'vl_result_availiable',
                'reason_vl_not_availiable',
                'reason_vl_not_availiable_other',
                'value_vl_size',
                'value_vl',
                'recent_vl_date',
                'any_new_diagnoses',
                'new_other_diagnoses']}
         ), audit_fieldset_tuple)

    radio_fields = {'info_since_lastvisit': admin.VERTICAL,
                    'laboratory_information_available': admin.VERTICAL,
                    'last_visit_result': admin.VERTICAL,
                    'reason_cd4_not_availiable': admin.VERTICAL,
                    'vl_result_availiable': admin.VERTICAL,
                    'reason_vl_not_availiable': admin.VERTICAL,
                    'value_vl_size': admin.VERTICAL,
                    'any_new_diagnoses': admin.VERTICAL, }

    custom_form_labels = {
        FormLabel(
            field='info_since_lastvisit',
            label='Since the last visit ({previous}) did you go for IDCC review?',
            previous_appointment=True
        ),
        FormLabel(
            field='last_visit_result',
            label='Is there a CD4 result since last visit ({previous}) ?',
            previous_appointment=True
        ),
        FormLabel(
            field='vl_result_availiable',
            label='Is there a VL result since last visit ({previous}) ?',
            previous_appointment=True
        ),
    }

    def format_form_label(self, label=None, instance=None, appointment=None, **kwargs):

        previous_instance = self.get_previous_instance(request=self.request)
        previous_appointment = self.get_previous_appt_instance(
            appointment=self.get_appointment(request=self.request)
        )

        previous = None

        if previous_instance:
            previous = previous_instance.report_datetime.date()
        elif previous_appointment:
            previous = previous_appointment.maternalvisit.report_datetime.date()

        label = label.format(previous=previous or 'Unknown')

        return label

    def get_model_data(self, request, object_id=None):

        subject_identifier = None

        self.request = request

        if self.get_instance(request):
            subject_identifier = self.get_instance(request).subject_identifier
        elif object_id:
            subject_identifier = self.get_object(
                request, object_id).maternal_visit.subject_identifier

        return self.maternal_hiv_interimhx_obj

    @property
    def subject_identifier(self):
        subject_identifier = None
        if self.get_instance(self.request):
            subject_identifier = self.get_instance(
                self.request).subject_identifier

        return subject_identifier

    @property
    def maternal_hiv_interimhx_obj(self):

        if self.subject_identifier:
            try:
                return MaternalHivInterimHx.objects.get(
                    maternal_visit__appointment__subject_identifier=self.subject_identifier)
            except MaternalHivInterimHx.DoesNotExist:
                pass

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['interimhx'] = self.get_model_data(request)
        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['interimhx'] = self.get_model_data(request, object_id)
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
