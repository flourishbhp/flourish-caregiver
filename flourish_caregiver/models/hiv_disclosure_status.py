from django.db import models

from edc_constants.choices import YES_NO
from edc_base.model_fields import OtherCharField
from .model_mixins import CrfModelMixin

from ..choices import REASONS_NOT_DISCLOSED


class HIVDisclosureStatusMixin(CrfModelMixin):

    associated_child_identifier = models.CharField(
        max_length=25)

    disclosed_status = models.CharField(
        verbose_name='Have you disclosed your HIV status to your child?',
        max_length=7,
        choices=YES_NO)

    plan_to_disclose = models.CharField(
        verbose_name='Do you plan on disclosing your HIV status to your '
                     'child?',
        max_length=7,
        blank=True,
        null=True,
        choices=YES_NO)

    reason_not_disclosed = models.CharField(
        verbose_name='What is the reason you have not disclosed your HIV '
                     'status to your child?',
        max_length=50,
        blank=True,
        null=True,
        choices=REASONS_NOT_DISCLOSED)

    reason_not_disclosed_other = OtherCharField()

    class Meta(CrfModelMixin.Meta):
        abstract = True


class HIVDisclosureStatusA(HIVDisclosureStatusMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'HIV Disclosure status A'
        verbose_name_plural = 'HIV Disclosure statusA'


class HIVDisclosureStatusB(HIVDisclosureStatusMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'HIV Disclosure statusB'
        verbose_name_plural = 'HIV Disclosure statusB'


class HIVDisclosureStatusC(HIVDisclosureStatusMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'HIV Disclosure statusC'
        verbose_name_plural = 'HIV Disclosure statusC'
