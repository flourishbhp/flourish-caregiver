from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_maternal_admin
from ..forms import FoodFrequencyQuestionnaireForm
from ..models import FoodFrequencyQuestionnaire


@admin.register(FoodFrequencyQuestionnaire, site=flourish_maternal_admin)
class FoodFrequencyQuestionnaireAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = FoodFrequencyQuestionnaireForm

    fieldsets = (
        (None, {
            'fields': [
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
