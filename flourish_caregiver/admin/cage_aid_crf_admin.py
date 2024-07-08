from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from flourish_caregiver.admin.modeladmin_mixins import CrfModelAdminMixin
from flourish_caregiver.admin_site import flourish_caregiver_admin
from flourish_caregiver.models import CaregiverCageAid
from flourish_caregiver.forms import CaregiverCageAidForm


@admin.register(CaregiverCageAid, site=flourish_caregiver_admin)
class CaregiverCageAidFormAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverCageAidForm

    fieldsets = (
        (None, {
            'fields': (
                'maternal_visit',
                'report_datetime',
                'alcohol_drugs',
                'cut_down',
                'people_reaction',
                'guilt',
                'eye_opener',

            )}
         ), audit_fieldset_tuple)

    radio_fields = {
        'alcohol_drugs': admin.VERTICAL,
        'cut_down': admin.VERTICAL,
        'people_reaction': admin.VERTICAL,
        'guilt': admin.VERTICAL,
        'eye_opener': admin.VERTICAL,
    }
