from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future

from flourish_caregiver.choices import ARV_DRUG_LIST


class MaternalArvTableMixin(BaseUuidModel):
    """ Inline ARV table to indicate ARV medication taken by mother """

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


    class Meta:
        unique_together = ('arv_code', 'start_date')
        abstract = True
