from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO

from flourish_caregiver.choices import BREAST_COLLECTED_CHOICES, EXP_COUNT_CHOICES, \
    NOT_COLLECTED_REASONS_CHOICES, YES_RESOLVED_NO
from . import CrfModelMixin


class BreastMilkFieldsMixin(CrfModelMixin, models.Model):
    exp_mastitis = models.CharField(
        verbose_name="Since the last FLOURISH visit (birth visit), has the participant "
                     "experienced mastitis?",
        choices=YES_RESOLVED_NO,
        max_length=35,
        null=True
    )

    exp_mastitis_count = models.CharField(
        verbose_name="How many times has the participant experienced mastitis since the "
                     "last visit?",
        max_length=10,
        choices=EXP_COUNT_CHOICES,
        null=True,
        blank=True
    )

    exp_cracked_nipples = models.CharField(
        verbose_name='Has the participant experienced cracked nipples since the last '
                     'FLOURISH visit?',
        choices=YES_NO,
        max_length=10,
        null=True,
        blank=False
    )

    exp_cracked_nipples_count = models.CharField(
        verbose_name="How many times has the participant experienced cracked nipples?",
        max_length=10,
        choices=EXP_COUNT_CHOICES,
        null=True,
        blank=True
    )

    milk_collected = models.CharField(
        verbose_name='Were you able to collect breast milk today?',
        choices=YES_NO,
        max_length=10,
        null=True,
        blank=True
    )

    not_collected_reasons = models.CharField(
        verbose_name='What was the reason for inability to collect breast milk today',
        choices=NOT_COLLECTED_REASONS_CHOICES,
        max_length=50,
        null=True,
        blank=True
    )

    breast_collected = models.CharField(
        verbose_name='Which breast was the collection from:',
        choices=BREAST_COLLECTED_CHOICES,
        max_length=30,
        null=True,
        blank=True
    )

    milk_collected_volume = models.IntegerField(
        verbose_name='Approximately how much breast milk was collected?(mL)',
        help_text='range from 1mL to 20mL',
        validators=[MinValueValidator(4), MaxValueValidator(20), ],
        null=True,
        blank=True
    )

    last_breastfed = models.DateTimeField(
        verbose_name='What date and time was the infant last breastfed ',
        null=True,
        blank=True
    )

    recently_ate = models.CharField(
        verbose_name="Did the mother have a meal in the past two hours ",
        max_length=10,
        choices=YES_NO,
        blank=True,
        null=True
    )

    add_comments = models.TextField(
        verbose_name='Any additional comments ',
        null=True,
        blank=True
    )
