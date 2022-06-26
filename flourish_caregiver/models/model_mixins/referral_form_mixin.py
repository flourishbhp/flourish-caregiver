from django.db import models
from edc_base.model_fields import OtherCharField

from ...choices import REFERRED_TO


class ReferralFormMixin(models.Model):
    referred_to = models.CharField(
        verbose_name='Referred To',
        choices=REFERRED_TO,
        max_length=50,
        null=True)

    referred_to_other = OtherCharField()


    class Meta:
        app_label = 'flourish_caregiver'
