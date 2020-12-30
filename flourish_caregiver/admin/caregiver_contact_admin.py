from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverContactForm
from ..models import CaregiverContact


@admin.register(CaregiverContact, site=flourish_caregiver_admin)
class CaregiverContactAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CaregiverContactForm

    search_fields = ['study_maternal_identifier']

    fieldsets = (
        (None, {
            'fields': ('study_maternal_identifier',
                       'prev_study',
                       'contact_date',
                       'contact_mode',
                       'contact_mode_other',
                       'phone_num_type',
                       'phone_num_success',
                       'cell_contact_fail',
                       'alt_cell_contact_fail',
                       'tel_contact_fail',
                       'alt_tel_contact_fail',
                       'work_contact_fail',
                       'cell_alt_contact_fail',
                       'tel_alt_contact_fail',
                       'cell_resp_person_fail',
                       'tel_resp_person_fail',
                       'home_visit_success',
                       'home_visit_fail',
                       'home_visit_fail_other')},
         ),
        audit_fieldset_tuple
    )

    radio_fields = {'contact_mode': admin.VERTICAL,
                    'cell_contact_fail': admin.VERTICAL,
                    'alt_cell_contact_fail': admin.VERTICAL,
                    'tel_contact_fail': admin.VERTICAL,
                    'alt_tel_contact_fail': admin.VERTICAL,
                    'work_contact_fail': admin.VERTICAL,
                    'cell_alt_contact_fail': admin.VERTICAL,
                    'tel_alt_contact_fail': admin.VERTICAL,
                    'cell_resp_person_fail': admin.VERTICAL,
                    'tel_resp_person_fail': admin.VERTICAL,
                    'home_visit_success': admin.VERTICAL,
                    'home_visit_fail': admin.VERTICAL}

    filter_horizontal = ('phone_num_type', 'phone_num_success')

    list_display = (
        'study_maternal_identifier', 'prev_study', 'contact_date', )
