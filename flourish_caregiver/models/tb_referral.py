from django.db import models
from edc_constants.choices import YES_NO

from flourish_caregiver.models.model_mixins import CrfModelMixin, ReferralFormMixin


class TbReferral(ReferralFormMixin, CrfModelMixin):
    referral_question = models.CharField(
        verbose_name='Were you referred to a TB clinic at this study visit? ',
        choices=YES_NO,
        max_length=10,
        null=True
    )


    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Referral'
        verbose_name_plural = 'TB Referrals'
