from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import ScreeningPregWomenForm
from ..models import ScreeningPregWomen


@admin.register(ScreeningPregWomen, site=flourish_caregiver_admin)
class ScreeningPregWomenAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ScreeningPregWomenForm

    search_fields = ['screening_identifier']

    fieldsets = (
        (None, {
            'fields': ('screening_identifier',
                       'report_datetime',
                       'hiv_testing',
                       'breastfeed_intent', )},
         ),
        audit_fieldset_tuple
    )

    radio_fields = {'hiv_testing': admin.VERTICAL,
                    'breastfeed_intent': admin.VERTICAL, }

    list_display = (
        'screening_identifier', 'report_datetime', 'is_eligible', 'is_consented')

    list_filter = ('report_datetime', 'is_eligible', 'is_consented')
