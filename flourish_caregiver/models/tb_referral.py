from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from flourish_caregiver.maternal_choices import GC_DHMT_CLINICS
from flourish_caregiver.models.model_mixins import CrfModelMixin, ReferralFormMixin


class TbReferral(ReferralFormMixin, CrfModelMixin):
    referral_question = models.CharField(
        verbose_name='Were you referred to a TB clinic at this study visit? ',
        choices=YES_NO,
        max_length=10,
        null=True
    )
    referral_clinic = models.CharField(
        verbose_name='Which clinic were you referred to?',
        choices=GC_DHMT_CLINICS,
        max_length=30,
        null=True
    )

    referral_clinic_other = OtherCharField()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Referral'
        verbose_name_plural = 'TB Referrals'
