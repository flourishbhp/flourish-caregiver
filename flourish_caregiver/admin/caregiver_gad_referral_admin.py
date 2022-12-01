from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverGadReferralForm
from ..models import CaregiverGadReferral
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CaregiverGadReferral, site=flourish_caregiver_admin)
class CaregiverGadReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverGadReferralForm

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
