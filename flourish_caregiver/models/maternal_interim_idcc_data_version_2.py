from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators.date import date_not_future
from edc_constants.choices import YES_NO

from ..maternal_choices import SIZE_CHECK_WITHOUT_EQUAL, \
    REASON_CD4_RESULT_UNAVAILABLE, REASON_VL_RESULT_UNAVAILABLE
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

    reason_cd4_not_availiable = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name="What is the reason a CD4 result is not available?",
        choices=REASON_CD4_RESULT_UNAVAILABLE)

    reason_cd4_not_availiable_other = OtherCharField()

    recent_cd4 = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Value of most recent CD4 available")

    recent_cd4_date = models.DateField(
        verbose_name="Date of CD4",
        validators=[date_not_future],
        blank=True,
        null=True)

    vl_result_availiable = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        verbose_name="Is there a VL result since last visit (visit date)?",
        choices=YES_NO)

    reason_vl_not_availiable = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name="What is the reason VL result is not available?",
        choices=REASON_VL_RESULT_UNAVAILABLE)

    reason_vl_not_availiable_other = OtherCharField()


    value_vl_size = models.CharField(
        max_length=25,
        verbose_name="Is the VL value “< or >”",
        choices=SIZE_CHECK_WITHOUT_EQUAL,
        blank=True,
        null=True)

    value_vl = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Value of  the most recent  available VL")

    recent_vl_date = models.DateField(
        verbose_name="Date of VL",
        validators=[date_not_future],
        blank=True,
        null=True)

    any_new_diagnoses = models.CharField(
        max_length=3,
        verbose_name="Is there any other new diagnoses in your last IDCC review?",
        choices=YES_NO,
        blank=True,
        null=True)

    new_other_diagnoses = models.TextField(
        max_length=25,
        verbose_name="Please specify other new diagnosis",
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = "Maternal Interim Idcc Data Version 2"
        verbose_name_plural = "Maternal Interim Idcc Data Version 2"
