from django.db import models

from .model_mixins import CrfModelMixin
from ..choices import YES_NO_UNK_DWTA, COUGH_DURATION, COVID_RESULTS, MONTH_YEAR


class TbVisitScreeningWomen(CrfModelMixin):
    have_cough = models.CharField(
        verbose_name='Do you currently have a cough?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    cough_duration = models.CharField(
        verbose_name='What is the duration of your cough?',
        choices=COUGH_DURATION,
        max_length=30,
        blank=True,
        null=True
    )

    cough_intersects_preg = models.CharField(
        verbose_name=('Did you have a cough more than 2 weeks ago, including during '
                      'pregnancy or shortly after delivery?'),
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    cough_timing = models.CharField(
        verbose_name='Enter timing of cough',
        choices=MONTH_YEAR,
        blank=True,
        null=True,
        max_length=30)

    cough_intersects_preg_cough_duration = models.CharField(
        verbose_name='What was the duration of that cough?',
        choices=COUGH_DURATION,
        max_length=30)

    fever = models.CharField(
        verbose_name='Do you currently have a fever?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    fever_during_preg = models.CharField(
        verbose_name=('Did you have a fever other than right now during pregnancy'
                      'to 2 months postpartum?'),
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    fever_timing = models.CharField(
        verbose_name='Enter timing of fever',
        choices=MONTH_YEAR,
        blank=True,
        null=True,
        max_length=30)

    night_sweats = models.CharField(
        verbose_name='Do you currently have night sweats?',
        choices=YES_NO_UNK_DWTA,
        help_text=(' A patient is considered to have night sweats if they have had more '
                   'than two nights of waking up with their night clothing drenched due '
                   'to sweating with a need to change the night clothing'),
        max_length=30)

    night_sweats_postpartum = models.CharField(
        verbose_name=('Did you have night sweats at any time during pregnancy to 2 months'
                      ' postpartum? '),
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    night_sweats_timing = models.CharField(
        verbose_name='Enter timing of night sweats',
        choices=MONTH_YEAR,
        blank=True,
        null=True,
        max_length=30)

    weight_loss = models.CharField(
        verbose_name='Do you currently have any unexplained weight loss?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    weight_loss_postpartum = models.CharField(
        verbose_name=('Did you have any unexplained weight loss during pregnancy to '
                      '2 months postpartum? '),
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    weight_loss_timing = models.CharField(
        verbose_name='Enter timing of weight loss',
        choices=MONTH_YEAR,
        blank=True,
        null=True,
        max_length=30)

    cough_blood = models.CharField(
        verbose_name='Have you coughed up blood in the last 2 weeks?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    cough_blood_postpartum = models.CharField(
        verbose_name=('Did you cough up blood at a time other than right now during '
                      'pregnancy to 2 months postpartum? '),
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    cough_blood_timing = models.CharField(
        verbose_name='Enter timing of coughing blood',
        choices=MONTH_YEAR,
        blank=True,
        null=True,
        max_length=30)

    enlarged_lymph_nodes = models.CharField(
        verbose_name='Do you currently have enlarged lymph nodes?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    enlarged_lymph_nodes_postpartum = models.CharField(
        verbose_name=('Did you have enlarged lymph nodes during pregnancy to 2 '
                      'months postpartum? '),
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    lymph_nodes_timing = models.CharField(
        verbose_name='Enter timing of enlarged lymph nodes',
        choices=MONTH_YEAR,
        blank=True,
        null=True,
        max_length=30)

    unexplained_fatigue = models.CharField(
        verbose_name='Do you currently have unexplained fatigue?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    unexplained_fatigue_postpartum = models.CharField(
        verbose_name=('Did you have unexplained fatigue during pregnancy to '
                      '2 months postpartum? '),
        choices=YES_NO_UNK_DWTA,
        blank=True,
        null=True,
        max_length=30)

    unexplained_fatigue_timing = models.CharField(
        verbose_name='Enter timing of unexplained fatigue',
        choices=MONTH_YEAR,
        blank=True,
        null=True,
        max_length=30)

    covid_19_test = models.CharField(
        verbose_name=('You reported having symptoms of [cough] [fever] today and/or'
                      ' during pregnancy to 2 months postpartum. When you experienced '
                      'these symptoms, were you tested for COVID-19? '),
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    received_results = models.CharField(
        verbose_name='did you receive the result(s)?',
        choices=YES_NO_UNK_DWTA,
        blank=True,
        null=True,
        max_length=10)

    covid_19_test_results = models.CharField(
        verbose_name='If yes, what were the results? ',
        choices=COVID_RESULTS,
        blank=True,
        null=True,
        max_length=30)

    tb_clinic_postpartum = models.CharField(
        verbose_name=('Were you referred to a TB clinic during pregnancy to 2 months'
                      ' postpartum? '),
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Screen at 2 months Postpartum'
        verbose_name_plural = 'TB Screen at 2 months Postpartum'
