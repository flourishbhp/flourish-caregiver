from django.db import models

from .model_mixins import CrfModelMixin
from ..choices import MEALS, FOOD_FREQUENCY, HOW_OFTEN


class FoodFrequencyQuestionnaire(CrfModelMixin):

    did_food_last = models.CharField(
        max_length=60,
        verbose_name="The food that (I/we) bought just didn’t last, "
                     "and (I/we) didn’t have money to get more.",
        choices=FOOD_FREQUENCY)

    afford_balanced_meals = models.CharField(
        max_length=50,
        verbose_name="(I/we) couldn’t afford to eat balanced meals.",
        choices=FOOD_FREQUENCY)

    cut_meals = models.CharField(
        max_length=50,
        verbose_name="In the last 12 months, since last (name of current "
                     "month), did (you/you or other adults in your household) "
                     "ever cut the size of your meals or skip meals because "
                     "there wasn't enough money for food?",
        choices=MEALS)

    how_often = models.CharField(
        max_length=60,
        verbose_name="How often did this happen—almost every month, some "
                     "months but not every month, or in only 1 or 2 months?",
        choices=HOW_OFTEN)

    ate_less = models.CharField(
        max_length=60,
        verbose_name="In the last 12 months, did you ever eat less than you "
                     "felt you should because there wasn't enough money for "
                     "food? ",
        choices=MEALS)

    no_food_money = models.CharField(
        max_length=60,
        verbose_name="In the last 12 months, were you every hungry but didn't "
                     "eat because there wasn't enough money for food?",
        choices=MEALS)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Food Frequency Questionnaire'
