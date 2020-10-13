from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future

from ..choices import ARV_DRUG_LIST, REASON_ARV_STOP
from .maternal_arv_preg import MaternalArvPreg


class ArvsDuringPregnancy(BaseUuidModel):

    """ Inline ARV table to indicate ARV medication taken by mother """

    maternal_arv_preg = models.ForeignKey(MaternalArvPreg, on_delete=PROTECT)

    arv_code = models.CharField(
        verbose_name="ARV code",
        max_length=35,
        choices=ARV_DRUG_LIST,
        help_text='Regimen has to be at least 3.')

    start_date = models.DateField(
        verbose_name="Date Started",
        validators=[date_not_future],
        null=True,
        blank=False,
        help_text='WARNING: If date started is less than 4 weeks at delivery, '
        'complete off study.')

    stop_date = models.DateField(
        verbose_name="Date Stopped",
        validators=[date_not_future],
        null=True,
        blank=True)

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
        app_label = 'flourish_maternal'
        verbose_name = 'ARVs During Pregnancy'
        verbose_name_plural = 'ARVs During Pregnancy'
        unique_together = ('maternal_arv_preg', 'arv_code', 'start_date')
