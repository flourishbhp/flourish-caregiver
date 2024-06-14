from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO,YES_NO_NA

from .list_models import DisclosureReasons
from .model_mixins import CrfModelMixin
from ..choices import DIFFICULTY_CHOICES, REACTION_CHOICES, REASONS_NOT_DISCLOSED, \
    WHODISCLOSED_CHOICES


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

    # Version 2 changes

    disclosure_age = models.PositiveIntegerField(
        verbose_name='At what age did you disclose your HIV status to your child?',
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(18)]
    )

    who_disclosed = models.CharField(
        verbose_name="Who disclosed this information to your child",
        max_length=20,
        blank=True,
        null=True,
        choices=WHODISCLOSED_CHOICES)

    who_disclosed_other = OtherCharField()

    disclosure_difficulty = models.CharField(
        verbose_name="How easy or difficult was it to disclose your HIV status to your "
                     "child?",
        max_length=20,
        blank=True,
        null=True,
        choices=DIFFICULTY_CHOICES)

    child_reaction = models.TextField(
        verbose_name='What was the reaction of the child after disclosure? (select all '
                     'that apply)',
        blank=True,
        null=True,
        choices=REACTION_CHOICES)

    child_reaction_other = OtherCharField()

    disclosure_intentional = models.CharField(
        verbose_name='Did your child find out about your HIV status (disclosure) '
                     'because you or another person you designated, intentionally told '
                     'them?',
        max_length=3,
        default='',
        choices=YES_NO_NA, )

    unintentional_disclosure_reason = models.ManyToManyField(
        DisclosureReasons,
        verbose_name='If this disclosure was unintentional, please provide reasons '
                     'why:',
        max_length=50,
        blank=True, )

    unintentional_disclosure_other = models.TextField(
        blank=True,
        null=True)

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
