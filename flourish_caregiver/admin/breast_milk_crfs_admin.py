from django.contrib import admin
from edc_constants.constants import OTHER
from edc_list_data import PreloadData, PreloadDataError
from edc_model_admin import audit_fieldset_tuple

from flourish_caregiver.admin.modeladmin_mixins import CrfModelAdminMixin
from flourish_caregiver.admin_site import flourish_caregiver_admin
from flourish_caregiver.forms import BreastMilk6MonthsForms, BreastMilkBirthForms
from flourish_caregiver.models import BreastMilk6Months, BreastMilkBirth


class BreastMilkAdminMixin(CrfModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'maternal_visit',
                'report_datetime',
                'exp_mastitis',
                'exp_mastitis_count',
                'mastitis_1_date_onset',
                'mastitis_1_type',
                'mastitis_1_action',
                'mastitis_1_action_other',
                'mastitis_2_date_onset',
                'mastitis_2_type',
                'mastitis_2_action',
                'mastitis_2_action_other',
                'mastitis_3_date_onset',
                'mastitis_3_type',
                'mastitis_3_action',
                'mastitis_3_action_other',
                'mastitis_4_date_onset',
                'mastitis_4_type',
                'mastitis_4_action',
                'mastitis_4_action_other',
                'mastitis_5_date_onset',
                'mastitis_5_type',
                'mastitis_5_action',
                'mastitis_5_action_other',
                'exp_cracked_nipples',
                'exp_cracked_nipples_count',
                'cracked_nipples_1_date_onset',
                'cracked_nipples_1_type',
                'cracked_nipples_1_action',
                'cracked_nipples_1_action_other',
                'cracked_nipples_2_date_onset',
                'cracked_nipples_2_type',
                'cracked_nipples_2_action',
                'cracked_nipples_2_action_other',
                'cracked_nipples_3_date_onset',
                'cracked_nipples_3_type',
                'cracked_nipples_3_action',
                'cracked_nipples_3_action_other',
                'cracked_nipples_4_date_onset',
                'cracked_nipples_4_type',
                'cracked_nipples_4_action',
                'cracked_nipples_4_action_other',
                'cracked_nipples_5_date_onset',
                'cracked_nipples_5_type',
                'cracked_nipples_5_action',
                'cracked_nipples_5_action_other',
                'milk_collected',
                'not_collected_reasons',
                'breast_collected',
                'milk_collected_volume',
                'last_breastfed',
                'add_comments',

            )}
         ), audit_fieldset_tuple)

    radio_fields = {
        'exp_mastitis': admin.VERTICAL,
        'exp_mastitis_count': admin.VERTICAL,
        'mastitis_1_type': admin.VERTICAL,
        'mastitis_2_type': admin.VERTICAL,
        'mastitis_3_type': admin.VERTICAL,
        'mastitis_4_type': admin.VERTICAL,
        'mastitis_5_type': admin.VERTICAL,
        'exp_cracked_nipples': admin.VERTICAL,
        'exp_cracked_nipples_count': admin.VERTICAL,
        'cracked_nipples_1_type': admin.VERTICAL,
        'cracked_nipples_2_type': admin.VERTICAL,
        'cracked_nipples_3_type': admin.VERTICAL,
        'cracked_nipples_4_type': admin.VERTICAL,
        'cracked_nipples_5_type': admin.VERTICAL,
        'milk_collected': admin.VERTICAL,
        'not_collected_reasons': admin.VERTICAL,
        'breast_collected': admin.VERTICAL,
    }

    filter_horizontal = (
        'mastitis_1_action',
        'mastitis_2_action',
        'mastitis_3_action',
        'mastitis_4_action',
        'mastitis_5_action',
        'cracked_nipples_1_action',
        'cracked_nipples_2_action',
        'cracked_nipples_3_action',
        'cracked_nipples_4_action',
        'cracked_nipples_5_action',
    )

    def extract_actions(self, field):
        action_key = ''
        if field.startswith("mastitis_"):
            action_number = field.split("_")[1]
            action_key = f"m{action_number}"
        elif field.startswith("cracked_nipples_"):
            action_number = field.split("_")[2]
            action_key = f"cn{action_number}"

        return action_key

    def generate_data(self, action_key):
        return [
            (f'{action_key}_both_breasts', 'Breastfeed from both breasts'),
            (f'{action_key}_uninfected_breast',
             'Breastfed from uninfected breast and pumped and dumped from the '
             'affected breast'),
            (f'{action_key}_stopped_breastfeeding', 'Stopped breastfeeding'),
            (f'{action_key}_temp_stopped',
             'Stopped breastfeeding temporarily but resumed once breast healed'),
            (f'{action_key}_{OTHER}', 'Other')
        ]

    def add_view(self, request, form_url='', extra_context=None):
        self.load_list_data(request)
        return super().add_view(request, form_url, extra_context)

    def load_list_data(self, request):
        for field in self.filter_horizontal:
            list_data = {}
            action = self.extract_actions(field)
            list_data[f'flourish_caregiver.mestitis{action}actions'] = (
                self.generate_data(action))
            try:
                PreloadData(list_data=list_data)
            except PreloadDataError:
                continue


@admin.register(BreastMilkBirth, site=flourish_caregiver_admin)
class BreastMilkBirthAdmin(BreastMilkAdminMixin, admin.ModelAdmin):
    form = BreastMilkBirthForms


@admin.register(BreastMilk6Months, site=flourish_caregiver_admin)
class BreastMilk6MonthsAdmin(BreastMilkAdminMixin, admin.ModelAdmin):
    form = BreastMilk6MonthsForms
