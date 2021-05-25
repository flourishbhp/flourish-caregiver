from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from ..maternal_choices import CURRENT_OCCUPATION, MONEY_PROVIDER, MONEY_EARNED
from ..maternal_choices import MARITAL_STATUS, ETHNICITY, HIGHEST_EDUCATION
from .model_mixins import CrfModelMixin


class SocioDemographicData(CrfModelMixin):

    """ A model completed by the user on Demographics form for all mothers.
    """

    marital_status = models.CharField(
        max_length=25,
        verbose_name="Current Marital status ",
        choices=MARITAL_STATUS)

    marital_status_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,)

    ethnicity = models.CharField(
        max_length=25,
        verbose_name="Ethnicity ",
        choices=ETHNICITY)

    ethnicity_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,)

    highest_education = models.CharField(
        max_length=25,
        verbose_name="Highest educational level completed ",
        choices=HIGHEST_EDUCATION)

    current_occupation = models.CharField(
        max_length=75,
        verbose_name="Current occupation",
        choices=CURRENT_OCCUPATION)

    current_occupation_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,)

    provides_money = models.CharField(
        max_length=50,
        verbose_name="Who provides most of your money?",
        choices=MONEY_PROVIDER)

    provides_money_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,)

    money_earned = models.CharField(
        max_length=50,
        verbose_name="How much money do you personally earn? ",
        choices=MONEY_EARNED)

    money_earned_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,)

    stay_with_child = models.CharField(
        verbose_name=(
            'Are you currently living in the same household as child '
            'who is also participating in the FLOURISH study?'),
        max_length=3,
        choices=YES_NO)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = "Socio Demographic Data"
        verbose_name_plural = "Socio Demographic Data"
