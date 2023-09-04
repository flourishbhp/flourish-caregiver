from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_visit_tracking.model_mixins import CrfInlineModelMixin

from .antenatal_enrollment import AntenatalEnrollment
from .list_models import ExpenseContributors
from .model_mixins import CrfModelMixin
from ..maternal_choices import CURRENT_OCCUPATION, MONEY_EARNED, MONEY_PROVIDER
from ..maternal_choices import ETHNICITY, HIGHEST_EDUCATION, MARITAL_STATUS


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
        null=True, )

    ethnicity = models.CharField(
        max_length=25,
        verbose_name="Ethnicity ",
        choices=ETHNICITY)

    ethnicity_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True, )

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
        null=True, )

    provides_money = models.CharField(
        max_length=50,
        verbose_name="Who provides most of your money?",
        choices=MONEY_PROVIDER)

    provides_money_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True, )

    money_earned = models.CharField(
        max_length=50,
        verbose_name="How much money do you personally earn? ",
        choices=MONEY_EARNED)

    money_earned_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True, )

    stay_with_child = models.CharField(
        verbose_name=(
            'Are you currently living in the same household as child '
            'who is also participating in the FLOURISH study?'),
        max_length=3,
        choices=YES_NO_NA)

    number_of_household_members = models.PositiveSmallIntegerField(
        verbose_name='How many household members live in the your primary home/ '
                     'compound?',
        help_text='A household member is considered someone who spends more nights on '
                  'average in your household than '
                  'in any other household in the same community over the last 12 months ',
        validators=[MinValueValidator(1), MaxValueValidator(25)],
        null=True,
        blank=True

    )

    contributes_to_expenses = models.CharField(
        verbose_name=(
            'Is there anyone else in the household who contributes to supporting the '
            'family expenses?'),
        max_length=3,
        null=True,
        choices=YES_NO)

    expense_contributors = models.ManyToManyField(
        ExpenseContributors,
        verbose_name='Who in the household contributes to supporting the family '
                     'expenses:',
        blank=True
    )

    expense_contributors_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True)

    """Quartely phone calls stem question"""
    socio_demo_changed = models.CharField(
        verbose_name='Has any of your following socio demographic data changed?',
        max_length=3,
        choices=YES_NO,
        null=True)

    @property
    def is_pregnant(self):
        return AntenatalEnrollment.objects.filter(
            subject_identifier=self.subject_identifier).exists()

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = "Socio Demographic Data"
        verbose_name_plural = "Socio Demographic Data"


class HouseHoldDetails(CrfInlineModelMixin, BaseUuidModel):
    """ Applicable for twins living in different households.
    """

    parent_model_attr = 'socio_demographics_data'

    socio_demographics_data = models.ForeignKey(
        SocioDemographicData, on_delete=models.CASCADE)

    child_identifier = models.CharField(
        verbose_name='Child Identifier',
        max_length=50, )

    stay_with_child = models.CharField(
        verbose_name=(
            'Are you currently living in the same household as child '
            'who is also participating in the FLOURISH study?'),
        max_length=3,
        choices=YES_NO_NA)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Household Details'
        verbose_name_plural = 'Household Details'
        unique_together = (
            ('socio_demographics_data', 'child_identifier'),)
