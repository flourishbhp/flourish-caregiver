from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from .modeladmin_mixins import CrfModelAdminMixin
from ..models import MaternalSocialWorkReferral
from ..forms import MaternalSocialWorkReferralForm


@admin.register(MaternalSocialWorkReferral, site=flourish_caregiver_admin)
class MaternalSocialWorkReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    
    form = MaternalSocialWorkReferralForm
    fieldsets = (
        (None, {
            "fields": (
                'maternal_visit',
                'report_datetime',
                'is_preg',
                'current_hiv_status',
                'referral_reason',
                'reason_other',
                'comment',
                
            ),
        }),audit_fieldset_tuple
    )
    
    radio_fields = {
        'is_preg': admin.VERTICAL, 
        'current_hiv_status': admin.VERTICAL, }



