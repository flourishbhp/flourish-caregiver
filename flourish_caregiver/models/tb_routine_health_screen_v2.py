from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField

from ..choices import TB_SCREENING_LOCATION, YES_NO_UNK_DWTA, VISIT_NUMBER
from .list_models import TbVisitCareLocation
from .model_mixins import CrfModelMixin


class TbRoutineHealthScreenV2(CrfModelMixin):
    tb_health_visits = models.CharField(
        verbose_name='How many health visits did you have in the last year since last study visit?',
        max_length=20,
        choices=VISIT_NUMBER,
        help_text='if 0, end of CRF. If 1 or greater, embed follow up questions for each visit.'
    )

    screen_location = models.ManyToManyField(
        TbVisitCareLocation,
        null=True,
        blank=True,
        verbose_name="For visit #1, where did you receive care",
    )

    screen_location_other = models.TextField(
        verbose_name='If other, specify',
        max_length=150,
        blank=True,
        null=True)

    tb_screened = models.CharField(
        verbose_name='Did you screen positive for TB at this visit because'
                     ' you had cough, fever, weight loss, '
                     'and/or night sweats?',
        max_length=20,
        choices=YES_NO_UNK_DWTA)

    diagnostic_referral = models.CharField(
        verbose_name='Were you referred to another clinic for further evaluation'
                     ' or did you receive testing during '
                     'that visit to see if you had tuberculosis?',
        max_length=20,
        null=True,
        blank=True,
        choices=YES_NO_UNK_DWTA)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Screen for TB at routine health encounters version 2'
        verbose_name_plural = 'Screen for TB at routine health encounters version 2'
