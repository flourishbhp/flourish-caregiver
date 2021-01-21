from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import HIVRapidTestCounselingForm
from ..models import HIVRapidTestCounseling
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HIVRapidTestCounseling, site=flourish_caregiver_admin)
class HIVRapidTestCounselingAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HIVRapidTestCounselingForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'rapid_test_done',
                'result_date',
                'result',
                'comments']}
         ), audit_fieldset_tuple)

    list_display = ('maternal_visit',
                    'rapid_test_done',
                    'result')
    list_filter = ('rapid_test_done', 'result')
    search_fields = ('result_date', )
    radio_fields = {"rapid_test_done": admin.VERTICAL,
                    "result": admin.VERTICAL, }
