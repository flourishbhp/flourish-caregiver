from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import TbInterviewTranslationForm
from ..models import TbInterviewTranslation
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(TbInterviewTranslation, site=flourish_caregiver_admin)
class TbInterviewTranslationAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TbInterviewTranslationForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'translation_date',
                'translator_name',
                'interview_translation',
            ]}
         ), audit_fieldset_tuple)
