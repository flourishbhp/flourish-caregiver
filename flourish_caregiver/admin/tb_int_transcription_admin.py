from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import TbInterviewTranscriptionForm
from ..models import TbInterviewTranscription
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(TbInterviewTranscription, site=flourish_caregiver_admin)
class TbInterviewTranscriptionAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TbInterviewTranscriptionForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'transcription_date',
                'transcriber_name',
                'interview_transcription'
            ]}
         ), audit_fieldset_tuple)
