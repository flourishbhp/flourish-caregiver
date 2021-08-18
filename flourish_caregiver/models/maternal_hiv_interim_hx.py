from django.core.validators import RegexValidator
from django.db import models
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from .model_mixins import CrfModelMixin


class MaternalHivInterimHx(CrfModelMixin):

    """ Laboratory and other clinical information collected during labor
    and delivery.
    for HIV +ve mothers ONLY
    """

    has_cd4 = models.CharField(
        verbose_name=("During this pregnancy did the mother have at least"
                      " one CD4 count performed (outside the study)? "),
        max_length=3,
        choices=YES_NO)

    cd4_date = models.DateField(
        verbose_name="Date of most recent CD4 test? ",
        validators=[date_not_future, ],
        blank=True,
        null=True)

    cd4_result = models.CharField(
        verbose_name="Result of most recent CD4 test",
        max_length=35,
        blank=True,
        null=True)

    has_vl = models.CharField(
        verbose_name=("During this pregnancy did the mother have a viral "
                      "load perfomed (outside the study)? "),
        max_length=3,
        choices=YES_NO,
        help_text="(if 'YES' continue. Otherwise go to question 9)")

    vl_date = models.DateField(
        verbose_name="If yes, Date of most recent VL test? ",
        validators=[date_not_future, ],
        blank=True,
        null=True)

    vl_detectable = models.CharField(
        verbose_name="Was the viral load detectable?",
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    vl_result = models.CharField(
        verbose_name="Result of most recent VL test",
        max_length=35,
        validators=[RegexValidator(r'^[0-9]*$', 'Viral load can only be a number'),],
        blank=True,
        null=True)

    comment = models.TextField(
        verbose_name="Comment if any additional pertinent information ",
        max_length=250,
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = "Maternal HIV Interim Hx"
        verbose_name_plural = "Maternal HIV Interim Hx"
