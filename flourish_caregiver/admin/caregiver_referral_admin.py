from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverReferralForm
from ..models import CaregiverReferral


@admin.register(CaregiverReferral, site=flourish_caregiver_admin)
class CaregiverReferralAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CaregiverReferralForm

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
