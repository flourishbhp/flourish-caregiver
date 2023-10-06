from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO

from .list_models import ArvInterruptionReasons
from .model_mixins import CrfModelMixin


class MaternalArvPostAdherence(CrfModelMixin):

    """
    This model is only for women living with HIV
    """

    missed_arv = models.PositiveIntegerField(
        default=0,
        verbose_name='Since the last 7 days, how many doses of ARVs have you missed or not taken?',
        help_text='Default answer to “0” in a numeric field',
        validators=[MinValueValidator(0), MaxValueValidator(7)]
    )

    interruption_reason = models.ManyToManyField(
        ArvInterruptionReasons,
        verbose_name='Please give reason for missing or not taking ART')

    interruption_reason_other = models.TextField(
        max_length=250,
        verbose_name='If Other, specify ',
        blank=True,
        null=True)

    comment = models.TextField(
        verbose_name='Comments',
        blank=True,
        null=True
    )

    """ Version 2 Questions added 06-Oct-2023 by amediphoko
    """
    stopped_art_past_yr = models.CharField(
        verbose_name=('In the last year, have you ever stopped taking '
                      'ART/treatment continuously for 7 days or more?'),
        max_length=3,
        choices=YES_NO)

    stopped_art_freq = models.PositiveIntegerField(
        verbose_name=('How many times have you stopped taking ART/treatment '
                      'continuously for 7 days or more?'),
        default=0)

    stopped_art_reasons = models.ManyToManyField(
        ArvInterruptionReasons,
        related_name='stopped_art_reasons',
        verbose_name=('Please give reason for why you stopped taking '
                      'ART/treatment continuously for 7 days or more'))

    stopped_reasons_other = models.TextField(
        verbose_name='If Other, specify ',
        max_length=250,
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Maternal ARVs Post Adherence: Version 2'
        verbose_name_plural = 'Maternal ARVs Post Adherence: Version 2'
