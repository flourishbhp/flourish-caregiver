from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import TbReferralForm
from ..models import TbReferral


@admin.register(TbReferral, site=flourish_caregiver_admin)
class TbReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = TbReferralForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'referral_question',
                'referred_to',
                'referred_to_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'referral_question': admin.VERTICAL, 'referred_to': admin.VERTICAL, }
