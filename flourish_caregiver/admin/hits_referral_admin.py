from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import HITSReferralForm
from ..models import HITSReferral
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HITSReferral, site=flourish_caregiver_admin)
class HITSReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HITSReferralForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'referred_to',
                'referred_to_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'referred_to': admin.VERTICAL}
