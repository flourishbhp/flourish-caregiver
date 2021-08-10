from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverLocatorForm
from ..models import CaregiverLocator
from .modeladmin_mixins import ModelAdminMixin
from flourish_caregiver.models import MaternalDataset
from django.shortcuts import redirect, reverse
from django.conf import settings


@admin.register(CaregiverLocator, site=flourish_caregiver_admin)
class CaregiverLocatorAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = CaregiverLocatorForm

    def response_add(self, request, obj):
        return redirect(settings.DASHBOARD_URL_NAMES.get('subject_listboard_url'))

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
        'has_caretaker': admin.VERTICAL}

    search_fields = ['subject_identifier', 'study_maternal_identifier']

    list_display = ('study_maternal_identifier', 'subject_identifier', 'may_visit_home', 'may_call',
                    'may_call_work')
