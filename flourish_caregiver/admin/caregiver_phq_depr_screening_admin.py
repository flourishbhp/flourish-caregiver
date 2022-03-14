from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverPhqDeprScreeningForm
from ..models import CaregiverPhqDeprScreening


@admin.register(CaregiverPhqDeprScreening, site=flourish_caregiver_admin)
class CaregiverPhqDeprScreeningAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = CaregiverPhqDeprScreeningForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'activity_interest',
                'depressed',
                'sleep_disorders',
                'fatigued',
                'eating_disorders',
                'self_doubt',
                'easily_distracted',
                'restlessness',
                'self_harm',
                'depression_score'
            ]}
         ), audit_fieldset_tuple)

    additional_instructions = (
        'Over the last 2 weeks, how often have you been bothered by any '
        'of the following problems?'
    )

    radio_fields = {'activity_interest': admin.VERTICAL,
                    'depressed': admin.VERTICAL,
                    'sleep_disorders': admin.VERTICAL,
                    'fatigued': admin.VERTICAL,
                    'eating_disorders': admin.VERTICAL,
                    'self_doubt': admin.VERTICAL,
                    'easily_distracted': admin.VERTICAL,
                    'restlessness': admin.VERTICAL,
                    'self_harm': admin.VERTICAL, }

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        return ('depression_score',) + fields
