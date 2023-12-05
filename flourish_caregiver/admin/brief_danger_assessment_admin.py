from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from flourish_caregiver.admin.modeladmin_mixins import CrfModelAdminMixin
from flourish_caregiver.admin_site import flourish_caregiver_admin
from flourish_caregiver.forms import BriefDangerAssessmentForm
from flourish_caregiver.models import BriefDangerAssessment


@admin.register(BriefDangerAssessment, site=flourish_caregiver_admin)
class BriefDangerAssessmentAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = BriefDangerAssessmentForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'physical_violence_increased',
                'used_weapons',
                'capable_of_killing',
                'choke',
                'partner_violently',
                'child_been_physically_hurt',
                'last_time_child_hurt_datetime',
                'last_time_child_hurt_estimated',
                'fear_partner_hurt_child',
            ]}
         ), audit_fieldset_tuple
    )

    radio_fields = {
        'physical_violence_increased': admin.VERTICAL,
        'used_weapons': admin.VERTICAL,
        'capable_of_killing': admin.VERTICAL,
        'choke': admin.VERTICAL,
        'partner_violently': admin.VERTICAL,
        'last_time_child_hurt_estimated': admin.VERTICAL,
        'child_been_physically_hurt': admin.VERTICAL,
        'fear_partner_hurt_child': admin.VERTICAL,
    }
