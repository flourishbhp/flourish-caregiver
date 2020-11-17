from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import SubstanceUsePriorPregnancyForm
from ..models import SubstanceUsePriorPregnancy
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SubstanceUsePriorPregnancy, site=flourish_caregiver_admin)
class SubstanceUsePriorPregnancyAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SubstanceUsePriorPregnancyForm

    list_display = (
        'maternal_visit',
        'smoked_prior_to_preg',
        'smoking_prior_preg_freq',
        'alcohol_prior_pregnancy',
        'alcohol_prior_preg_freq',
        'marijuana_prior_preg',
        'marijuana_prior_preg_freq',
    )

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'smoked_prior_to_preg',
                'smoking_prior_preg_freq',
                'alcohol_prior_pregnancy',
                'alcohol_prior_preg_freq',
                'marijuana_prior_preg',
                'marijuana_prior_preg_freq',
                'khat_prior_preg',
                'khat_prior_preg_freq',
                'other_illicit_substances_prior_preg']}
         ), audit_fieldset_tuple)

    radio_fields = {
        'smoked_prior_to_preg': admin.VERTICAL,
        'smoking_prior_preg_freq': admin.VERTICAL,
        'alcohol_prior_pregnancy': admin.VERTICAL,
        'alcohol_prior_preg_freq': admin.VERTICAL,
        'marijuana_prior_preg': admin.VERTICAL,
        'marijuana_prior_preg_freq': admin.VERTICAL,
        'khat_prior_preg': admin.VERTICAL,
        'khat_prior_preg_freq': admin.VERTICAL
    }
