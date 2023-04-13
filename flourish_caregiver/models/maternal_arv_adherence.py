from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO

from .list_models import ArvInterruptionReasons
from .model_mixins import CrfModelMixin


class MaternalArvAdherence(CrfModelMixin):

    """
    This model is only for women living with HIV at enrolment visit (1000M or 2000M)
    """

    missed_arv = models.PositiveIntegerField(
        verbose_name='Since last 7days, how many doses of ART have you missed or not taken?',
        default=0,
        help_text='Default answer to “0” in a numeric field',
        validators=[MinValueValidator(0), MaxValueValidator(7)],
    )

    interruption_reason = models.ManyToManyField(
        ArvInterruptionReasons,
        related_name='interruption_reason',
        verbose_name='Please give reason for missing or not taking ART', )

    interruption_reason_other = models.TextField(
        verbose_name='If Other, specify',
        max_length=250,
        blank=True,
        null=True)

    art_defaulted = models.CharField(
        verbose_name=('In the last year, have you ever stopped taking ART/treatment '
                      'continuously for 7 days or more?'),
        choices=YES_NO,
        max_length=3, )

    days_defaulted = models.PositiveIntegerField(
        verbose_name=('If yes to Q6, how many times have you stopped taking ART/treatment '
                      'continuously for 7 days or more?'),
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        blank=True,
        null=True
    )

    reason_defaulted = models.ManyToManyField(
        ArvInterruptionReasons,
        related_name='reason_defaulted',
        verbose_name=('Please give reason for why you stopped taking ART/treatment '
                      'continuously for 7 days or more'), )

    reason_defaulted_other = models.TextField(
        verbose_name='If Other, specify',
        max_length=250,
        blank=True,
        null=True)

    comment = models.TextField(
        verbose_name='Comments',
        blank=True,
        null=True
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Maternal ARVs Adherence'
        verbose_name_plural = 'Maternal ARVs Adherence'
