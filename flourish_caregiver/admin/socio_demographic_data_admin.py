from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import SocioDemographicDataForm
from ..models import SocioDemographicData
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SocioDemographicData, site=flourish_caregiver_admin)
class SocioDemographicDataAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SocioDemographicDataForm

    list_display = ('maternal_visit',
                    'marital_status',
                    'ethnicity',
                    'highest_education')
    list_filter = ('marital_status',
                   'ethnicity',
                   'highest_education')

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'marital_status',
                'marital_status_other',
                'ethnicity',
                'ethnicity_other',
                'highest_education',
                'current_occupation',
                'current_occupation_other',
                'provides_money',
                'provides_money_other',
                'money_earned',
                'money_earned_other',
                'stay_with_child']}
         ), audit_fieldset_tuple)

    radio_fields = {'marital_status': admin.VERTICAL,
                    'ethnicity': admin.VERTICAL,
                    'highest_education': admin.VERTICAL,
                    'current_occupation': admin.VERTICAL,
                    'provides_money': admin.VERTICAL,
                    'money_earned': admin.VERTICAL,
                    'stay_with_child': admin.VERTICAL}

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
