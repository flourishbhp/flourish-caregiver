from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_caregiver_admin
from .modeladmin_mixins import CrfModelAdminMixin
from ..models import CaregiverSocialWorkReferral
from ..forms import CaregiverSocialWorkReferralForm


@admin.register(CaregiverSocialWorkReferral, site=flourish_caregiver_admin)
class CaregiverSocialWorkReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverSocialWorkReferralForm

    fieldsets = (
        (None, {
            "fields": (
                'maternal_visit',
                'report_datetime',
                'referral_for',
                'is_preg',
                'current_hiv_status',
                'child_exposure_status',
                'referral_reason',
                'reason_other',
                'comment',

            ),
        }), audit_fieldset_tuple
    )

    radio_fields = {
        'referral_for': admin.VERTICAL,
        'is_preg': admin.VERTICAL,
        'current_hiv_status': admin.VERTICAL,
        'child_exposure_status': admin.VERTICAL}

    filter_horizontal = ('referral_reason',)
