from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from ..choices import ARV_INTERRUPTION_REASON
from .model_mixins import CrfModelMixin


class MaternalArvDuringPreg(CrfModelMixin):

    """ This model is for all HIV positive mothers who are pregnant
    (whom we hope to enroll their infant) and/or for mothers who
    have just delivered
    """

    took_arv = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Did the mother receive any ARVs during this pregnancy?",
        help_text="(NOT including single -dose NVP in labour)")

    is_interrupt = models.CharField(
        max_length=3,
        choices=YES_NO_NA,
        verbose_name="Was there an interruption in the ARVs received during "
        "pregnancy through delivery of >/=3days?",
    )

    interrupt = models.CharField(
        verbose_name="Please give reason for interruption",
        max_length=50,
        choices=ARV_INTERRUPTION_REASON,
        default=NOT_APPLICABLE)

    interrupt_other = models.TextField(
        max_length=250,
        verbose_name="Other, specify ",
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'ARVs During Pregnancy'
        verbose_name_plural = 'ARVs During Pregnancy'
