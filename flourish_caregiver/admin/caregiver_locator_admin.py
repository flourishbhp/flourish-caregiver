from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverLocatorForm
from ..models import CaregiverLocator
from .modeladmin_mixins import ModelAdminMixin
from edc_fieldsets import Fieldsets
from flourish_caregiver.models import MaternalDataset
from django.shortcuts import redirect, reverse
from django.conf import settings
from ..models import SubjectConsent
from django.http import HttpResponseRedirect


@admin.register(CaregiverLocator, site=flourish_caregiver_admin)
class CaregiverLocatorAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = CaregiverLocatorForm

    def response_add(self, request, obj, **kwargs):
        response = self._redirector(obj)
        return response if response else super(CaregiverLocatorAdmin, self).response_add(request, obj)

    def response_change(self, request, obj):
        response = self._redirector(obj)
        return response if response else super(CaregiverLocatorAdmin, self).response_change(request, obj)

    def _redirector(self, obj):
        caregiver_locator = SubjectConsent.objects.filter(subject_identifier=obj.subject_identifier)
        if caregiver_locator:
            return HttpResponseRedirect(f'/subject/subject_dashboard/{obj.subject_identifier}/')

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'screening_identifier',
                'study_maternal_identifier',
                'report_datetime',
                'locator_date',
                'first_name',
                'last_name',
                'mail_address',
                'health_care_infant',
                'may_visit_home',
                'physical_address',
                'may_call',
                'subject_cell',
                'subject_cell_alt',
                'subject_phone',
                'subject_phone_alt',
                'may_call_work',
                'subject_work_place',
                'subject_work_phone',
                'may_contact_indirectly',
                'indirect_contact_name',
                'indirect_contact_relation',
                'indirect_contact_physical_address',
                'indirect_contact_cell',
                'indirect_contact_phone',
                'has_caretaker',
                'caretaker_name',
                'caretaker_cell',
                'caretaker_tel'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'may_call': admin.VERTICAL,
        'may_call_work': admin.VERTICAL,
        'may_visit_home': admin.VERTICAL,
        'may_contact_indirectly': admin.VERTICAL,
        'has_caretaker': admin.VERTICAL,
        'is_locator_updated': admin.VERTICAL,
    }

    search_fields = ['subject_identifier', 'study_maternal_identifier']

    list_display = ('study_maternal_identifier', 'subject_identifier', 'may_visit_home',
                    'may_call', 'may_call_work')


    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)
        subject_identifier = getattr(obj, 'subject_identifier', '')
        if subject_identifier and 'P' in subject_identifier:
            fieldsets = Fieldsets(fieldsets=fieldsets)
            try:
                fieldsets.insert_fields(*('is_locator_updated',), insert_after='caretaker_tel')
            except AttributeError:
                pass
            else:
                return fieldsets.fieldsets
        return fieldsets
