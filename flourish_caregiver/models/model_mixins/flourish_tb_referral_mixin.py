from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future

from flourish_caregiver.choices import CLINIC_NAMES, TB_REASON_CHOICES


class TBReferralMixin(models.Model):

    date_of_referral = models.DateField(
        verbose_name='Date of referral:',
        validators=[date_not_future],
        blank=True,
        null=True
    )

    reason_for_referral = models.CharField(
        verbose_name='Reason for referral:',
        choices=TB_REASON_CHOICES,
        max_length=50,
        blank=True,
        null=True)

    reason_for_referral_other = models.TextField(
        verbose_name='If other, specify:',
        max_length=255,
        blank=True,
        null=True)

    clinic_name = models.CharField(
        verbose_name='Clinic names:',
        choices=CLINIC_NAMES,
        max_length=50,
        blank=True,
        null=True)

    clinic_name_other = OtherCharField(
        verbose_name='If other, specify', )

    class Meta:
        abstract = True
