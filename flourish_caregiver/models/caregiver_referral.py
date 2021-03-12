from django.db import models
from edc_base.model_fields import OtherCharField

from ..choices import REFERRED_TO
from .model_mixins import CrfModelMixin


class CaregiverReferral(CrfModelMixin):

    referred_to = models.CharField(
        verbose_name='Referred To',
        choices=REFERRED_TO,
        max_length=50)

    referred_to_other = OtherCharField()

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Referral'
        verbose_name_plural = 'Caregiver Referral'
