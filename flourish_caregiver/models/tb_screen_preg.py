from django.db import models

from .model_mixins import CrfModelMixin
from ..choices import YES_NO_UNK_DWTA


class TbScreenPreg(CrfModelMixin):

    have_cough = models.CharField(
        verbose_name='Do you currently have a cough?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    cough_lasted_2wks = models.CharField(
        verbose_name='Has the cough lasted > 2 weeks?',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        blank=True,
        null=True)

    cough_blood_last_2wks = models.CharField(
        verbose_name='Have you coughed up blood in the last 2 weeks?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    have_fever = models.CharField(
        verbose_name='Do you currently have a fever?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    fever_lasted_2wks = models.CharField(
        verbose_name='Has the fever lasted > 2 weeks?',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        blank=True,
        null=True)

    have_night_sweats = models.CharField(
        verbose_name='Do you currently have night sweats?',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        help_text=('A patient is considered to have night sweats if they have '
                   'had more than two nights of waking up with their night '
                   'clothing drenched due to sweating with a need to change '
                   'the night clothing'))

    sweats_lasted_2wks = models.CharField(
        verbose_name='Has the night sweats lasted > 2 weeks?',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        blank=True,
        null=True)

    have_enlarged_lymph = models.CharField(
        verbose_name='Do you currently have enlarged lymph nodes?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    unexplained_fatigue = models.CharField(
        verbose_name='Do you have unexplained fatigue?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    unexplained_weight_loss = models.CharField(
        verbose_name='Do you have unexplained fatigue?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    weight_gain_fail = models.CharField(
        verbose_name='Have you had failure to gain weight during pregnancy?',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        null=True,
        blank=True)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Enrollment TB Screen for Pregnant Women'
        verbose_name_plural = 'Enrollment TB Screen for Pregnant Women'
