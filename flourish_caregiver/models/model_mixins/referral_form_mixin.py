from django.db import models
from edc_base.model_fields import OtherCharField

from ...choices import REFERRED_TO


<<<<<<< HEAD
class ReferralFormMixin:
=======
class ReferralFormMixin(models.Model):
>>>>>>> 10658e898b7115019c711a2fe54810d3c80a8eb5

    referred_to = models.CharField(
        verbose_name='Referred To',
        choices=REFERRED_TO,
        max_length=50)

    referred_to_other = OtherCharField()

    class Meta:
<<<<<<< HEAD
        app_label = 'flourish_caregiver'
=======
>>>>>>> 10658e898b7115019c711a2fe54810d3c80a8eb5
        abstract = True
