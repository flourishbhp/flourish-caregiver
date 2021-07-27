from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import HIVDisclosureStatusFormA, HIVDisclosureStatusFormB
from ..forms import HIVDisclosureStatusFormC, HIVDisclosureStatusFormD
from ..models import HIVDisclosureStatusA, HIVDisclosureStatusB
from ..models import HIVDisclosureStatusC, HIVDisclosureStatusD


class HIVDisclosureStatusAdminMixin(ModelAdminMixin, admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'disclosed_status',
                'plan_to_disclose',
                'reason_not_disclosed',
                'reason_not_disclosed_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'disclosed_status': admin.VERTICAL,
                    'reason_not_disclosed': admin.VERTICAL,
                    'plan_to_disclose': admin.VERTICAL}


@admin.register(HIVDisclosureStatusA, site=flourish_caregiver_admin)
class HIVDisclosureStatusAdminA(ModelAdminMixin, admin.ModelAdmin):

    form = HIVDisclosureStatusFormA


@admin.register(HIVDisclosureStatusB, site=flourish_caregiver_admin)
class HIVDisclosureStatusAdminB(ModelAdminMixin, admin.ModelAdmin):
    form = HIVDisclosureStatusFormB


@admin.register(HIVDisclosureStatusC, site=flourish_caregiver_admin)
class HIVDisclosureStatusAdminC(ModelAdminMixin, admin.ModelAdmin):
    form = HIVDisclosureStatusFormC


@admin.register(HIVDisclosureStatusD, site=flourish_caregiver_admin)
class HIVDisclosureStatusAdminD(ModelAdminMixin, admin.ModelAdmin):
    form = HIVDisclosureStatusFormD
