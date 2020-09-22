from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_maternal_admin
from ..forms import MaternalLocatorForm
from ..models import MaternalLocator
from .modeladmin_mixins import ModelAdminMixin


@admin.register(MaternalLocator, site=flourish_maternal_admin)
class MaternalLocatorAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = MaternalLocatorForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'screening_identifier',
                'report_datetime',
                'locator_date',
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

    search_fields = ['subject_identifier']

    list_display = ('subject_identifier', 'may_visit_home', 'may_call',
                    'may_call_work')
