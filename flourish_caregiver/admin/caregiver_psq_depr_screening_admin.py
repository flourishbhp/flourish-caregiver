from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverPsqDeprScreeningForm
from ..models import CaregiverPsqDeprScreening


@admin.register(CaregiverPsqDeprScreening, site=flourish_caregiver_admin)
class CaregiverPsqDeprScreeningAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverPsqDeprScreeningForm

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
                'self_harm'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'activity_interest': admin.VERTICAL,
                    'depressed': admin.VERTICAL,
                    'sleep_disorders': admin.VERTICAL,
                    'fatigued': admin.VERTICAL,
                    'eating_disorders': admin.VERTICAL,
                    'self_doubt': admin.VERTICAL,
                    'easily_distracted': admin.VERTICAL,
                    'restlessness': admin.VERTICAL,
                    'self_harm': admin.VERTICAL, }
