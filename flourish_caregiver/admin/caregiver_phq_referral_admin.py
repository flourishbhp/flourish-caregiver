from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverPhqReferralForm
from ..models import CaregiverPhqReferral
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CaregiverPhqReferral, site=flourish_caregiver_admin)
class CaregiverPhqReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverPhqReferralForm

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
