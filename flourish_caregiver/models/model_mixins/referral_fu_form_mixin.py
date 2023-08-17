from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from ...choices import PERCEIVE_COUNSELOR
from ...choices import YES_NO_PNTA, EMO_SUPPORT_DECLINE, NO_EMO_SUPPORT_REASON
from ..list_models import EmoSupportType, EmoHealthImproved


class ReferralFUFormMixin(models.Model):

    attended_referral = models.CharField(
        verbose_name=('Since you were referred for emotional support at the last attended '
                      'visit, have you been attended at a referred site?'),
        max_length=20,
        choices=YES_NO_PNTA)

    support_ref_decline_reason = models.CharField(
        verbose_name=('If no, what is the reason for not going for emotional support '
                      'referral?'),
        max_length=40,
        choices=EMO_SUPPORT_DECLINE,
        blank=True,
        null=True)

    support_ref_decline_reason_other = OtherCharField()

    emo_support = models.CharField(
        verbose_name=('If yes, did you receive emotional support?'),
        max_length=20,
        choices=YES_NO_PNTA,
        blank=True,
        null=True)

    no_support_reason = models.CharField(
        verbose_name=('If no, please share reason why you have not received emotional '
                      'support?'),
        max_length=50,
        choices=NO_EMO_SUPPORT_REASON,
        blank=True,
        null=True)

    no_support_reason_other = OtherCharField()

    emo_support_type = models.ManyToManyField(
        EmoSupportType,
        verbose_name=(
            'If yes, what kind of emotional support did you receive?'),
        blank=True)

    emo_support_type_other = OtherCharField()

    emo_health_improved = models.ManyToManyField(
        EmoHealthImproved,
        verbose_name=('Since you received emotional support, how has your emotional health '
                      'improved?'),
        blank=True)

    emo_health_improved_other = OtherCharField()

    percieve_counselor = models.CharField(
        verbose_name=(
            'How did you perceive your counselor (social worker or psychologist)?'),
        max_length=35,
        choices=PERCEIVE_COUNSELOR,
        blank=True,
        null=True)

    percieve_counselor_other = OtherCharField()

    satisfied_counselor = models.CharField(
        verbose_name=('Are you satisfied with your counselor?'),
        max_length=3,
        choices=YES_NO,
        blank=True,
        null=True)

    additional_counseling = models.CharField(
        verbose_name=('Would you also like us to provide a referral for additional'
                      ' counselling?'),
        max_length=3,
        choices=YES_NO,
        blank=True,
        null=True)

    class Meta:
        app_label = 'flourish_caregiver'
