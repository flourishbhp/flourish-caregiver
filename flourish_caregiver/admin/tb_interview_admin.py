from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import TbInterviewForm
from ..models import TbInterview
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(TbInterview, site=flourish_caregiver_admin)
class TbInterviewAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TbInterviewForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'interview_location',
                'interview_location_other',
                'interview_duration',
                'interview_file',
                'interview_language',

            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'interview_location': admin.VERTICAL,
                    'interview_language': admin.VERTICAL, }
