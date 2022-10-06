from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import TbEngagementForm
from ..models import TbEngagement
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(TbEngagement, site=flourish_caregiver_admin)
class TbEngagementAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TbEngagementForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'interview_consent',
                'interview_decline_reason',
                'interview_decline_reason_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'interview_consent': admin.VERTICAL,
        'interview_decline_reason': admin.VERTICAL}
