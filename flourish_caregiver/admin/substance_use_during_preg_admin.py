from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import SubstanceUseDuringPregnancyForm
from ..models import SubstanceUseDuringPregnancy
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SubstanceUseDuringPregnancy, site=flourish_caregiver_admin)
class SubstanceUseDuringPregnancyAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SubstanceUseDuringPregnancyForm

    list_display = (
        'maternal_visit',
        'smoked_during_preg',
        'smoking_during_preg_freq',
        'alcohol_during_pregnancy',
        'alcohol_during_preg_freq',
        'marijuana_during_preg',
        'marijuana_during_preg_freq',
    )

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'smoked_during_preg',
                'smoking_during_preg_freq',
                'alcohol_during_pregnancy',
                'alcohol_during_preg_freq',
                'marijuana_during_preg',
                'marijuana_during_preg_freq',
                'khat_during_preg',
                'khat_during_preg_freq',
                'other_illicit_substances_during_preg']}
         ), audit_fieldset_tuple)

    radio_fields = {
        'smoked_during_preg': admin.VERTICAL,
        'smoking_during_preg_freq': admin.VERTICAL,
        'alcohol_during_pregnancy': admin.VERTICAL,
        'alcohol_during_preg_freq': admin.VERTICAL,
        'marijuana_during_preg': admin.VERTICAL,
        'marijuana_during_preg_freq': admin.VERTICAL,
        'khat_during_preg': admin.VERTICAL,
        'khat_during_preg_freq': admin.VERTICAL
    }
