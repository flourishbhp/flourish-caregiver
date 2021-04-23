from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import ArvsPrePregnancyForm
from ..models import ArvsPrePregnancy
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(ArvsPrePregnancy, site=flourish_caregiver_admin)
class ArvsPrePregnancyAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = ArvsPrePregnancyForm

    list_filter = ('preg_on_art',)

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'prev_preg_azt',
                'prev_sdnvp_labour',
                'prev_preg_art',
                'art_start_date',
                'is_date_estimated',
                'preg_on_art',
                'art_changes',
                'prior_preg',
                'prior_arv',
                'prior_arv_other']}
         ), audit_fieldset_tuple)

    radio_fields = {
        'prev_preg_azt': admin.VERTICAL,
        'prev_sdnvp_labour': admin.VERTICAL,
        'prev_preg_art': admin.VERTICAL,
        'preg_on_art': admin.VERTICAL,
        'prior_preg': admin.VERTICAL,
        'is_date_estimated': admin.VERTICAL}

    filter_horizontal = ('prior_arv',)
