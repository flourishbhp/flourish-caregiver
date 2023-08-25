from django.db import models
from .model_mixins import CrfModelMixin
from ..choices import ARV_INTERRUPTION_REASON_POST_ADHERENCE


class MaternalArvPostAdherence(CrfModelMixin):

    """
    This model is only for women living with HIV
    """

    missed_arv = models.PositiveIntegerField(
        default=0,
        verbose_name='Since the last visit, how many doses of ARVs have you missed or not taken?',
        help_text='Default answer to “0” in a numeric field',
    )

    interruption_reason = models.CharField(
        verbose_name='Please give reason for interruption',
        max_length=50,
        choices=ARV_INTERRUPTION_REASON_POST_ADHERENCE,
    )

    interruption_reason_other = models.TextField(
        max_length=250,
        verbose_name="If Other, specify ",
        blank=True,
        null=True)

    comment = models.TextField(
        verbose_name="Comments",
        blank=True,
        null=True
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Maternal ARVs Post Adherence'
        verbose_name_plural = 'Maternal ARVs Post Adherence'
