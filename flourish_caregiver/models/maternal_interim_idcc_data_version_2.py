from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators.date import date_not_future
from edc_constants.choices import YES_NO

from ..maternal_choices import SIZE_CHECK
from .model_mixins import CrfModelMixin


class MaternalInterimIdccVersion2(CrfModelMixin):

    info_since_lastvisit = models.CharField(
        max_length=25,
        verbose_name="Is there new laboratory information available on the "
        "mother since last visit",
        choices=YES_NO)

    recent_cd4 = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Most recent CD4 available")

    recent_cd4_date = models.DateField(
        verbose_name="Date of recent CD4",
        validators=[date_not_future],
        blank=True,
        null=True)

    value_vl_size = models.CharField(
        max_length=25,
        verbose_name="Is the value for the most recent VL available “=” ,"
        "“<”, or “>” a number? ",
        choices=SIZE_CHECK,
        blank=True,
        null=True)

    value_vl = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Value of VL ")

    recent_vl_date = models.DateField(
        verbose_name="Date of recent VL",
        validators=[date_not_future],
        blank=True,
        null=True)

    other_diagnoses = OtherCharField(
        max_length=25,
        verbose_name="Please specify any other diagnoses found in the IDCC "
        "since the last visit ",
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = "Maternal Interim Idcc Data Version 2"
        verbose_name_plural = "Maternal Interim Idcc Data Version 2"
