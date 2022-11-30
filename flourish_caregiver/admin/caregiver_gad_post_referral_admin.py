from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverGadPostReferralForm
from ..models import CaregiverGadPostReferral
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CaregiverGadPostReferral, site=flourish_caregiver_admin)
class CaregiverGadPostReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverGadPostReferralForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'emo_support_provider',
                'emo_support_type',
                'emo_support_type_other',
                'emo_health_improved',
                'emo_health_improved_other',
                'percieve_counselor',
                'percieve_counselor_other',
                'satisfied_counselor',
                'additional_counseling'

            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'emo_support_provider': admin.VERTICAL,
                    'emo_health_improved': admin.VERTICAL,
                    'percieve_counselor': admin.VERTICAL,
                    'satisfied_counselor': admin.VERTICAL,
                    'additional_counseling': admin.VERTICAL, }

    filter_horizontal = ('emo_support_type',)
