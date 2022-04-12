from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField

from ..choices import TB_SCREENING_LOCATION, YES_NO_UNK_DWTA
from .model_mixins import CrfModelMixin


class TbRoutineHealthScreen(CrfModelMixin):

    tb_screened = models.CharField(
        verbose_name=(
            'Were you screened for TB at a routine healthcare encounter '
            'with the four screening questions (cough for 2 weeks, '
            'fever, weight loss, night sweats) since conception?'),
        max_length=20,
        choices=YES_NO_UNK_DWTA)

    screen_location = models.CharField(
        verbose_name='Where were you screened?',
        max_length=25,
        null=True,
        blank=True,
        choices=TB_SCREENING_LOCATION)

    screen_location_other = OtherCharField()

    pos_screen = models.CharField(
        verbose_name='Did you screen positive for the TB symptom screen?',
        max_length=20,
        null=True,
        blank=True,
        choices=YES_NO_UNK_DWTA)

    diagnostic_referral = models.CharField(
        verbose_name='Were you referred for TB diagnostic evaluation?',
        max_length=20,
        null=True,
        blank=True,
        choices=YES_NO_UNK_DWTA)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Screen for TB at routine health encounters'
        verbose_name_plural = 'Screen for TB at routine health encounters'
