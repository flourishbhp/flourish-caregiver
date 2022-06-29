from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import TbOffStudyForm
from ..models import TbOffStudy


@admin.register(TbOffStudy, site=flourish_caregiver_admin)
class TbOffStudyAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = TbOffStudyForm

    search_fields = ('subject_identifier',)

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'offstudy_date',
                'reason',
                'reason_other',
                'offstudy_point',
                'comment']}
         ), audit_fieldset_tuple)

    radio_fields = {'reason': admin.VERTICAL,
                    'offstudy_point': admin.VERTICAL}
