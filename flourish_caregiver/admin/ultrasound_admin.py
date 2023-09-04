from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_caregiver_admin
from ..forms import UltraSoundForm
from ..models import UltraSound
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(UltraSound, site=flourish_caregiver_admin)
class UltraSoundAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = UltraSoundForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'number_of_gestations',
                'bpd',
                'hc',
                'ac',
                'fl',
                'ga_by_lmp',
                'ga_by_ultrasound_wks',
                'ga_by_ultrasound_days',
                'ga_confirmed',
                'ga_at_consent',
                'est_fetal_weight',
                'est_edd_ultrasound',
                'edd_confirmed',
                'amniotic_fluid_volume', ]}
         ), audit_fieldset_tuple)

    readonly_fields = ('edd_confirmed', 'ga_confirmed', 'ga_by_lmp', 'ga_at_consent')

    radio_fields = {'number_of_gestations': admin.VERTICAL,
                    'amniotic_fluid_volume': admin.VERTICAL, }

    list_display = (
        'number_of_gestations', 'ga_confrimation_method', 'edd_confirmed',
        'ga_confirmed', 'ga_by_lmp')

    list_filter = ('maternal_visit',
                   'number_of_gestations',
                   'ga_confrimation_method')
