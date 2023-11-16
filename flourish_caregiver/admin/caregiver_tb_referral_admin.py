from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from flourish_caregiver.admin.modeladmin_mixins import CrfModelAdminMixin
from flourish_caregiver.admin_site import flourish_caregiver_admin
from flourish_caregiver.forms.caregiver_tb_referral_form import CaregiverTBReferralForm
from flourish_caregiver.models.caregiver_tb_referral import TBReferralCaregiver


@admin.register(TBReferralCaregiver, site=flourish_caregiver_admin)
class CaregiverTBReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = CaregiverTBReferralForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'referred_for_screening',
                'date_of_referral',
                'reason_for_referral',
                'reason_for_referral_other',
                'clinic_name',
                'clinic_name_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'reason_for_referral': admin.VERTICAL,
                    'clinic_name': admin.VERTICAL, }
