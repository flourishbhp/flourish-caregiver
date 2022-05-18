from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from .modeladmin_mixins import CrfModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverReferralForm
from ..models import CaregiverReferral


@admin.register(CaregiverReferral, site=flourish_caregiver_admin)
class CaregiverReferralAdmin(CrfModelAdminMixin):
    
    form = CaregiverReferralForm
    
    fieldsets = (
        (None, {
            "fields": (
                'maternal_visit',
                'report_datetime',
                'is_pregnant',
                'hiv_status',
                'referral_reason',
                'referred_other',
                'comment',
            ),
        }),
    )
    
    radio_fields = {
        'is_pregnant': admin.VERTICAL,
        'hiv_status': admin.VERTICAL,
    }
    
