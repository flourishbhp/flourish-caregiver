from django.db import models
from edc_constants.choices import YES_NO

from ..choices import DECLINE_REASON
from .model_mixins import CrfModelMixin


class TbEngagement(CrfModelMixin):

    interview_consent = models.CharField(
        verbose_name='Does participant agree to the interview?',
        choices=YES_NO,
        max_length=3,)

    interview_decline_reason = models.CharField(
        verbose_name='Provide reason for not undergoing the interview',
        choices=DECLINE_REASON,
        max_length=50,
        blank=True,
        null=True)

    interview_decline_reason_other = models.TextField(
        verbose_name='If other, specify',
        max_length=150,
        blank=True,
        null=True)

    class Meta:
        app_label = 'flourish_caregiver'
