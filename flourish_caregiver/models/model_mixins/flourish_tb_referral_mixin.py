from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO
from ..list_models import CaregiverTbReferralReasons
from flourish_caregiver.choices import CLINIC_NAMES, NO_REFERRAL_REASONS


class TBReferralMixin(models.Model):

    referred = models.CharField(
        verbose_name='Was a TB referral made?',
        choices=YES_NO,
        max_length=3)

    no_referral_reason = models.CharField(
        verbose_name='Reason for NO referral',
        choices=NO_REFERRAL_REASONS,
        max_length=20,
        null=True,
        blank=True)

    date_of_referral = models.DateField(
        verbose_name='Date of referral:',
        validators=[date_not_future],
        blank=True,
        null=True
    )

    reason_for_referral = models.ManyToManyField(
        CaregiverTbReferralReasons,
        related_name='reason_referral',
        verbose_name='Reason for referral:',
        blank=True
    )

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

    attend_flourish_clinic = models.CharField(
        verbose_name=('Is the participant able to come to '
                      'FLOURISH clinic for referral'),
        choices=YES_NO,
        max_length=3,
        null=True,
        blank=True)

    class Meta:
        abstract = True
