from django.db import models

from edc_constants.choices import YES_NO
from .model_mixins import CrfModelMixin


class HIVDisclosureStatus(CrfModelMixin):

    disclosed_status = models.CharField(
        verbose_name='Have you disclosed your HIV status to your child?',
        max_length=7,
        choices=YES_NO)

    plan_to_disclose = models.CharField(
        verbose_name='Do you plan on disclosing your HIV status to your '
                     'child?',
        max_length=7,
        choices=YES_NO)

    reason_not_disclosed = models.CharField(
        verbose_name='What is the reason you have not disclosed your HIV '
                     'status to your child?',
        max_length=50)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'HIV Disclosure status'
        verbose_name_plural = 'HIV Disclosure status'
