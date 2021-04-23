import calendar
from django.contrib import admin
from edc_base.utils import get_utcnow
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import FoodSecurityQuestionnaireForm
from ..models import FoodSecurityQuestionnaire


@admin.register(FoodSecurityQuestionnaire, site=flourish_caregiver_admin)
class FoodSecurityQuestionnaireAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = FoodSecurityQuestionnaireForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'did_food_last',
                'afford_balanced_meals',
                'cut_meals',
                'how_often',
                'ate_less',
                'no_food_money',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'did_food_last': admin.VERTICAL,
                    'afford_balanced_meals': admin.VERTICAL,
                    'cut_meals': admin.VERTICAL,
                    'how_often': admin.VERTICAL,
                    'ate_less': admin.VERTICAL,
                    'no_food_money': admin.VERTICAL}

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        curr_month = calendar.month_name[get_utcnow().month]
        custom_label = (f'In the last 12 months, since last {curr_month}, did '
                        '(you or other adults in your household) ever cut '
                        'the size of your meals or skip meals because there '
                        'wasn\'t enough money for food?')

        form.base_fields['cut_meals'].label = custom_label
        form = self.auto_number(form)
        return form
