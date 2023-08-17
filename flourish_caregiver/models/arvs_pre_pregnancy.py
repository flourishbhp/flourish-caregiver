from django.core.validators import MinValueValidator
from django.db import models
from edc_base.model_fields import IsDateEstimatedFieldNa, OtherCharField
from edc_base.model_validators.date import date_not_future
from edc_constants.choices import YES_NO, YES_NO_NA

from ..maternal_choices import PRIOR_PREG_ART_STATUS
from .list_models import PriorArv
from .model_mixins import CrfModelMixin


class ArvsPrePregnancy(CrfModelMixin):

    """ A model completed by the user on ARV history for infected mothers only.
    """

    prev_preg_azt = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Did she ever receive AZT monotherapy in a "
        "previous pregnancy?  ")

    prev_sdnvp_labour = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Did she ever receive single-dose NVP in labour "
        "during a previous pregnancy?")

    prev_preg_art = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=("Did she ever receive triple antiretrovirals during a "
                      "prior pregnancy?"))

    art_start_date = models.DateField(
        validators=[
            date_not_future, ],
        verbose_name="Date of triple antiretrovirals first started")

    is_date_estimated = IsDateEstimatedFieldNa(
        verbose_name=("Is the subject's date of triple antiretrovirals estimated?"))

    preg_on_art = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        verbose_name=("Was she still on triple antiretrovirals at the "
                      "time she became pregnant"
                      " for this pregnancy? "))

    art_changes = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="How many times did you change your triple "
        "antiretrovirals medicines?",
        help_text='If there was no change please enter 0.')

    prior_preg = models.CharField(
        max_length=80,
        verbose_name="Prior to this pregnancy the mother has ",
        choices=PRIOR_PREG_ART_STATUS)

    prior_arv = models.ManyToManyField(
        PriorArv,
        verbose_name=("Please list all of the ARVs that the mother "
                      "ever received prior to the current pregnancy:"))

    prior_arv_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = "ARVs Pre Pregnancy"
        verbose_name_plural = "ARVs Pre Pregnancy"
