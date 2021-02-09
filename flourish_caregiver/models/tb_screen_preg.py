from django.db import models

from edc_base.model_fields import OtherCharField

from .model_mixins import CrfModelMixin
from ..choices import WHERE_SCREENED, YES_NO_UNK_DWTA


class TbScreenPreg(CrfModelMixin):

    have_cough = models.CharField(
        verbose_name='Have you had a cough for ≥2 weeks?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    have_fever = models.CharField(
        verbose_name='Do you currently have a fever?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    night_sweats = models.CharField(
        verbose_name='Do you currently have night sweats?',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        help_text=('A patient is considered to have night sweats if they have '
                   'had more than two nights of waking up with their night '
                   'clothing drenched due to sweating with a need to change '
                   'the night clothing'))

    weight_loss = models.CharField(
        verbose_name='Do you have any unexplained weight loss?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    cough_blood = models.CharField(
        verbose_name='Have you coughed up blood in the last 2 weeks?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    enlarged_lymph = models.CharField(
        verbose_name='Do you currently have enlarged lymph nodes?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    unexplained_fatigue = models.CharField(
        verbose_name='Do you have unexplained fatigue?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    tb_screened = models.CharField(
        verbose_name='Were you screened for TB at a routine healthcare '
                     'encounter with the four screening questions (cough '
                     'for 2 weeks, fever, weight loss, night sweats) '
                     'since conception?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    where_screened = models.CharField(
        verbose_name='Where were you screened?',
        choices=WHERE_SCREENED,
        max_length=30)

    where_screened_other = OtherCharField(
        verbose_name='If other, specify')

    tb_symptom_screened = models.CharField(
        verbose_name='Did you screen positive for the TB symptom screen?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    diagnostic_evaluation = models.CharField(
        verbose_name='Were you referred for TB diagnostic evaluation? ',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Enrollment TB Screen for Pregnant Women'
        verbose_name_plural = 'Enrollment TB Screen for Pregnant Women'
