from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import MedicalHistoryForm
from ..models import MedicalHistory


@admin.register(MedicalHistory, site=flourish_caregiver_admin)
class MedicalHistoryAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MedicalHistoryForm

    list_display = ('maternal_visit', 'chronic_since', )
    list_filter = ('chronic_since', )

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'chronic_since',
                'caregiver_chronic',
                'caregiver_chronic_other',
                'who_diagnosis',
                'who',
                'caregiver_medications',
                'caregiver_medications_other',
                'know_hiv_status',
                'comment']}
         ), audit_fieldset_tuple)

    radio_fields = {'chronic_since': admin.VERTICAL,
                    'who_diagnosis': admin.VERTICAL,
                    'know_hiv_status': admin.VERTICAL}

    filter_horizontal = (
        'who', 'caregiver_chronic', 'caregiver_medications')
