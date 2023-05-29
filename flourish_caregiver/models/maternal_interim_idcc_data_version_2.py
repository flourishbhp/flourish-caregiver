from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators.date import date_not_future
from edc_constants.choices import YES_NO

from ..maternal_choices import SIZE_CHECK, REASON_CD4_NOT_COLLECTED
from .model_mixins import CrfModelMixin
from ..constants import BREASTFEED_ONLY, MISSED, NO_SAMPLE_COLLECTED,\
    NO_SAMPLE_TUBES, MACHINE_NOT_WORKING


class MaternalInterimIdccVersion2(CrfModelMixin):

    info_since_lastvisit = models.CharField(
        max_length=3,
        verbose_name="Since the last visit (VISIT DATE) did you go for IDCC review?",
        choices=YES_NO)

    laboratory_information_available = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        verbose_name="Is there new laboratory information available? ",
        choices=YES_NO)

    last_visit_result = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        verbose_name="Is there a CD4 result since last visit (visit date)?",
        choices=YES_NO)

    reason_cd4_not_collected = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name="What is the reason a CD4 result is not available?",
        choices=REASON_CD4_NOT_COLLECTED)

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
