from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalArvAdherenceForm
from ..models import MaternalArvAdherence


@admin.register(MaternalArvAdherence, site=flourish_caregiver_admin)
class MaternalArvAdherenceAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = MaternalArvAdherenceForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'missed_arv',
                'interruption_reason',
                'interruption_reason_other',
                'art_defaulted',
                'days_defaulted',
                'reason_defaulted',
                'reason_defaulted_other',
                'comment']}
         ), audit_fieldset_tuple)

    radio_fields = {'art_defaulted': admin.VERTICAL}

    filter_horizontal = ('interruption_reason', 'reason_defaulted')

    search_fields = ('subject_identifier',)

    list_display = ('maternal_visit', 'missed_arv',)
