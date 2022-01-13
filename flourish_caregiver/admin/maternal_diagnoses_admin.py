from django.contrib import admin
from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalDiagnosesForm
from ..models import MaternalDiagnoses
from .modeladmin_mixins import CrfModelAdminMixin
from edc_model_admin import audit_fieldset_tuple


@admin.register(MaternalDiagnoses, site=flourish_caregiver_admin)
class MaternalDiagnosesAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MaternalDiagnosesForm
    list_display = ('maternal_visit', 'has_who_dx')
    list_filter = ('has_who_dx',)
    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'new_diagnoses',
                'diagnoses',
                'diagnoses_other',
                'has_who_dx',
                'who']}
         ), audit_fieldset_tuple)

    radio_fields = {
        'has_who_dx': admin.VERTICAL,
        'new_diagnoses': admin.VERTICAL,
    }

    filter_horizontal = ('who','diagnoses')
