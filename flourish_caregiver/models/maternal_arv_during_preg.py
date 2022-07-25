from django.db import models
from django.db.models import PROTECT
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from .model_mixins import CrfModelMixin
from .model_mixins.martenal_arv_table_mixin import MaternalArvTableMixin
from ..choices import ARV_INTERRUPTION_REASON, REASON_ARV_STOP


class MaternalArvDuringPreg(CrfModelMixin):

    """ This model is for all HIV positive mothers who are pregnant
    (whom we hope to enroll their infant)
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


class MaternalArvTableDuringPreg(MaternalArvTableMixin):
    """ Inline ARV table to indicate ARV medication taken by mother """

    maternal_arv_durg_preg = models.ForeignKey(MaternalArvDuringPreg, on_delete=PROTECT)

    reason_for_stop = models.CharField(
        verbose_name="Reason for stop",
        choices=REASON_ARV_STOP,
        max_length=50,
        null=True,
        blank=True,
        help_text='If "Treatment Failure", notify study coordinator')

    reason_for_stop_other = models.TextField(
        max_length=250,
        verbose_name="Other, specify ",
        blank=True,
        null=True)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Maternal ARV Table During Pregnancy'
        verbose_name_plural = 'Maternal ARV Table During Pregnancy'
