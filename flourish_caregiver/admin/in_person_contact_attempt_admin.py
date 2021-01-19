from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import InPersonContactAttemptForm
from ..models import InPersonContactAttempt


@admin.register(InPersonContactAttempt, site=flourish_caregiver_admin)
class InPersonContactAttemptAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InPersonContactAttemptForm

    search_fields = ['study_maternal_identifier']

    fieldsets = (
        (None, {
            'fields': ('study_maternal_identifier',
                       'prev_study',
                       'contact_date',
                       'contact_location',
                       'successful_location',
                       'phy_addr_unsuc',
                       'phy_addr_unsuc_other',
                       'workplace_unsuc',
                       'workplace_unsuc_other',
                       'contact_person_unsuc',
                       'contact_person_unsuc_other', )},
         ),
        audit_fieldset_tuple
    )

    radio_fields = {'contact_location': admin.VERTICAL,
                    'successful_location': admin.VERTICAL,
                    'phy_addr_unsuc': admin.VERTICAL,
                    'workplace_unsuc': admin.VERTICAL,
                    'contact_person_unsuc': admin.VERTICAL}

    list_display = (
        'study_maternal_identifier', 'prev_study', 'contact_date', )
