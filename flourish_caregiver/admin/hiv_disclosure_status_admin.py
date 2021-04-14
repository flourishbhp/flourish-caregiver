from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import HIVDisclosureStatusForm
from ..models import HIVDisclosureStatus


@admin.register(HIVDisclosureStatus, site=flourish_caregiver_admin)
class HIVDisclosureStatusAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = HIVDisclosureStatusForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'disclosed_status',
                'plan_to_disclose',
                'reason_not_disclosed',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'disclosed_status': admin.VERTICAL,
                    'plan_to_disclose': admin.VERTICAL}
