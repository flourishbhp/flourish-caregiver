from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import HITSPostReferralForm
from ..models import HITSPostReferral
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HITSPostReferral, site=flourish_caregiver_admin)
class HITSPostReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HITSPostReferralForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'visited_referral_site',
                'reason_unvisited',
                'reason_unvisited_other',
                'received_support',
                'no_support_reason',
                'no_support_reason_other',
                'support_type',
                'support_type_other',
                'health_improved',
                'health_improved_other',
                'supp_member_percept',
                'supp_member_percept_other',
                'satisfied_w_clinic',
                'visit_helpful',
                'additional_counseling'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'visited_referral_site': admin.VERTICAL,
                    'received_support': admin.VERTICAL,
                    'no_support_reason': admin.VERTICAL,
                    'supp_member_percept': admin.VERTICAL,
                    'satisfied_w_clinic': admin.VERTICAL,
                    'visit_helpful': admin.VERTICAL,
                    'additional_counseling': admin.VERTICAL, }

    filter_horizontal = ('reason_unvisited', 'support_type', 'health_improved')
