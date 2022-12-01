from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverPhqReferralFUForm
from ..models import CaregiverPhqReferralFU
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CaregiverPhqReferralFU, site=flourish_caregiver_admin)
class CaregiverPhqReferralFUAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverPhqReferralFUForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'attended_referral',
                'support_ref_decline_reason',
                'support_ref_decline_reason_other',
                'emo_support',
                'no_support_reason',
                'no_support_reason_other',
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

    radio_fields = {'attended_referral': admin.VERTICAL,
                    'support_ref_decline_reason': admin.VERTICAL,
                    'emo_support': admin.VERTICAL,
                    'no_support_reason': admin.VERTICAL,
                    'emo_health_improved': admin.VERTICAL,
                    'percieve_counselor': admin.VERTICAL,
                    'satisfied_counselor': admin.VERTICAL,
                    'additional_counseling': admin.VERTICAL, }

    filter_horizontal = ('emo_support_type',)
