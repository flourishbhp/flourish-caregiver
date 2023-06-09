
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_constants.choices import YES_NO, POS_NEG_IND_UNKNOWN
from ..choices import HIV_TESTING_REFUSAL_REASON
from .model_mixins import CrfModelMixin
from edc_base.model_fields import OtherCharField


class CaregiverHivRapidTestAndConseling(CrfModelMixin):
    test_for_hiv = models.CharField(
        verbose_name='Have you tested for HIV since last visit or within last 3 months?',
        choices=YES_NO,
        max_length=3
    )

    date_of_test = models.DateField(
        verbose_name='Date of Rapid test',
        blank=True,
        null=True
    )

    test_results = models.CharField(
        verbose_name='What was the rapid test result?',
        choices=POS_NEG_IND_UNKNOWN,
        blank=True,
        null=True,
        max_length=15
    )

    reason_not_tested = models.CharField(
        verbose_name='Reason for not testing for HIV',
        choices=HIV_TESTING_REFUSAL_REASON,
        blank=True,
        null=True,
        max_length=35
    )

    reason_not_tested_other = OtherCharField(
        verbose_name='If ‘other’ specify',
    )

    comment = models.TextField(
        verbose_name='Any Comments in a text box',
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Post HIV rapid testing and counseling'
        verbose_name_plural = 'Post HIV rapid testing and counseling'
