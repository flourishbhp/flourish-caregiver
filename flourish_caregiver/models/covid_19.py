from edc_constants.choices import YES_NO, POS_NEG_IND_UNKNOWN, YES_NO_UNKNOWN

from .model_mixins import CrfModelMixin
from django.db import models
from ..choices import *
from .list_models import CovidSymptoms, CovidSymptomsAfter14Days


class Covid19(CrfModelMixin):
    test_for_covid = models.CharField(
        verbose_name='Have you been tested for COVID-19?',
        max_length=35,
        choices=YES_NO_COVID_FORM,
    )

    date_of_test = models.DateField(
        verbose_name='Date of the test',
        null=True,
        blank=True)

    is_test_estimated = models.CharField(
        verbose_name='Is this test estimated? ',
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True)

    reason_for_testing = models.CharField(
        verbose_name='What was the reason for testing?',
        choices=TESTING_REASONS,
        max_length=30,
        null=True,
        blank=True
    )

    other_reason_for_testing = models.CharField(
        verbose_name='Other reason for testing?',
        max_length=30,
        null=True,
        blank=True
    )

    result_of_test = models.CharField(
        verbose_name='What was the result of the test?',
        choices=POS_NEG_PENDING_UNKNOWN,
        max_length=30,
        null=True,
        blank=True
    )

    isolation_location = models.CharField(
        verbose_name='If your results were positive, where were you isolated? ',
        choices=ISOLATION_LOCATION,
        max_length=15,
        null=True,
        blank=True
    )

    other_isolation_location = models.CharField(
        verbose_name='If other, where were you isolated?',
        max_length=30,
        null=True,
        blank=True
    )

    isolations_symptoms = models.ManyToManyField(
        CovidSymptoms,
        verbose_name='Have you experienced any of the following signs and symptoms when on isolation',
        blank=True
    )

    has_tested_positive = models.CharField(
        verbose_name='Has anyone in your household tested positive for COVID-19',
        choices=YES_NO_UNKNOWN,
        max_length=15,

    )

    date_of_test_member = models.DateField(
        verbose_name='Date of the test for member of household',
        null=True,
        blank=True

    )

    is_test_estimated = models.CharField(
        verbose_name='Is this test estimated',
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True
    )

    close_contact = models.CharField(
        verbose_name='Have you been in close contact with anyone outside of your household who tested positive for '
                     'COVID-19',
        max_length=10,
        choices=YES_NO_UNKNOWN,
    )

    symptoms_for_past_14days = models.ManyToManyField(
        CovidSymptomsAfter14Days,
        verbose_name='In the last 14 days, have you experienced any of the following symptoms',
        blank=False
    )

    fully_vaccinated = models.CharField(
        verbose_name='Have you been fully vaccinated for COVID-19',
        max_length=25,
        choices=YES_NO_PARTIALLY
    )

    vaccination_type = models.CharField(
        verbose_name='Which vaccine did you receive',
        max_length=20,
        choices=VACCINATION_TYPE,
        null=True,
        blank=True
    )

    other_vaccination_type = models.CharField(
        verbose_name='If other specify which vaccine you received?',
        max_length=20,
        null=True,
        blank=True
    )

    first_dose = models.DateField(
        verbose_name='Date of first vaccine dose',
        null=True,
        blank=True
    )

    second_dose = models.DateField(
        verbose_name='Date of second vaccine dose',
        null=True,
        blank=True
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Covid-19 Form'
        verbose_name_plural = 'Caregiver Covid-19 Forms'
