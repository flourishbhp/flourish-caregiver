from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import PostHivRapidTestAndConselingForm
from ..models import PostHivRapidTestAndConseling
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(PostHivRapidTestAndConseling, site=flourish_caregiver_admin)
class PostHivRapidTestAndConselingAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PostHivRapidTestAndConselingForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'rapid_test_done',
                'result_date',
                'result',
                'reason_not_tested',
                'reason_not_tested_other',
                'comment',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'rapid_test_done': admin.VERTICAL,
        'result': admin.VERTICAL,
        'reason_not_tested': admin.VERTICAL,
    }
