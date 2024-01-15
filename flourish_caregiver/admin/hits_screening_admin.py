from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from flourish_caregiver.admin.modeladmin_mixins import CrfModelAdminMixin
from flourish_caregiver.admin_site import flourish_caregiver_admin
from flourish_caregiver.forms import HITSScreeningForm
from flourish_caregiver.models import HITSScreening


@admin.register(HITSScreening, site=flourish_caregiver_admin)
class HITSScreeningAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = HITSScreeningForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'physical_hurt',
                'insults',
                'threaten',
                'screem_curse',
                'score'
            ]}
         ), audit_fieldset_tuple
    )

    radio_fields = {
        'physical_hurt': admin.VERTICAL,
        'insults': admin.VERTICAL,
        'threaten': admin.VERTICAL,
        'screem_curse': admin.VERTICAL,
    }
