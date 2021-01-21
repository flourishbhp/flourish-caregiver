from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from ..maternal_choices import (
    WATER_SOURCE, COOKING_METHOD, TOILET_FACILITY, HOUSE_TYPE)
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

    own_phone = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Do you have your own cell phone that you use regularly?",
        blank=True,
        null=True,)

    water_source = models.CharField(
        max_length=50,
        verbose_name="At your primary home  where do you "
        "get most of your family's drinking water?",
        choices=WATER_SOURCE,
        help_text=("the home where you are likely to spend the"
                   " most time with your baby over the"
                   " first 18 months"),
        blank=True,
        null=True,)

    house_electrified = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Is there electricity in this house / compound? ",
        blank=True,
        null=True,)

    house_fridge = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Is there a refrigerator being used in this house "
        "/ compound?  ",
        blank=True,
        null=True,)

    cooking_method = models.CharField(
        max_length=50,
        verbose_name="What is the primary method of cooking in this house "
        "/ compound?",
        choices=COOKING_METHOD,
        blank=True,
        null=True,)

    toilet_facility = models.CharField(
        max_length=50,
        verbose_name=("Which of the following types of toilet facilities do "
                      "you most often use"
                      " at this house / compound? "),
        choices=TOILET_FACILITY,
        blank=True,
        null=True,)

    toilet_facility_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,)

    house_people_number = models.IntegerField(
        verbose_name="How many members live in your household?",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(25), ],
        help_text=('A household member is considered someone who spends more '
                   'nights on average in your household than in any other '
                   'household in the same community over the last 12 months'))

    house_members_18older = models.IntegerField(
        verbose_name=('Of the people who live in your household, how many are '
                      'older than 18?'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(25), ])

    house_type = models.CharField(
        max_length=50,
        verbose_name="Housing type?  ",
        choices=HOUSE_TYPE,
        help_text="Indicate the primary type of housing used over the past "
        "30 days",
        blank=True,
        null=True,)

    stay_with_child = models.CharField(
        verbose_name=('Are you currently living in the same household as child '
                      'who is also participating in the FLOURISH study?'),
        max_length=3,
        choices=YES_NO)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = "Socio Demographic Data"
        verbose_name_plural = "Socio Demographic Data"
