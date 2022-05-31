from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import TbStudyScreeningForm
from ..models import TbStudyScreening


@admin.register(TbStudyScreening, site=flourish_caregiver_admin)
class TbStudyScreeningAdmin(CrfModelAdminMixin):
    form = TbStudyScreeningForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'tb_participation'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'tb_participation': admin.VERTICAL, }
