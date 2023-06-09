from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverHivRapidTestAndConselingForm
from ..models import CaregiverHivRapidTestAndConseling
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CaregiverHivRapidTestAndConseling, site=flourish_caregiver_admin)
class CaregiverHivRapidTestAndConselingAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverHivRapidTestAndConselingForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'test_for_hiv',
                'date_of_test',
                'test_results',
                'reason_not_tested',
                'reason_not_tested_other',
                'comment',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'test_for_hiv': admin.VERTICAL,
        'test_results': admin.VERTICAL,
        'reason_not_tested': admin.VERTICAL,
    }
