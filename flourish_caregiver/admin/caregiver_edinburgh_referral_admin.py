from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from .modeladmin_mixins import CrfModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverEdinburghReferralForm
from ..models import CaregiverEdinburghReferral


@admin.register(CaregiverEdinburghReferral, site=flourish_caregiver_admin)
class CaregiverEdinburghReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverEdinburghReferralForm

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
