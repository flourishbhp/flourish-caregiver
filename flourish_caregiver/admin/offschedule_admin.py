from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverOffScheduleForm
from ..models import CaregiverOffSchedule
from .modeladmin_mixins import ModelAdminMixin


@admin.register(CaregiverOffSchedule, site=flourish_caregiver_admin)
class CaregiverOffScheduleAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CaregiverOffScheduleForm

    fieldsets = (
        (None, {
            'fields': [
                'schedule_name',
                'subject_identifier'
            ]}
         ), audit_fieldset_tuple)

    list_filter = ('schedule_name', 'subject_identifier',)
