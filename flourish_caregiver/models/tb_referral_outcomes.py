from django.db import models
from edc_constants.choices import YES_NO

from ..choices import YES_NO_UNABLE_DET
from .model_mixins import CrfModelMixin


class TbReferralOutcomes(CrfModelMixin):

    referral_clinic_appt = models.CharField(
        verbose_name='Did participant go to the TB clinic to which they were referred',
        max_length=3,
        choices=YES_NO)

    further_tb_eval = models.CharField(
        verbose_name=('Did the participant go to any clinic for further TB evaluation '
                      'after they were referred?'),
        max_length=3,
        choices=YES_NO)

    tb_diagnostic_perf = models.CharField(
        verbose_name=('Were TB diagnostic studies performed at the clinic visit?'),
        max_length=20,
        choices=YES_NO_UNABLE_DET,
        null=True,
        blank=True)

        # tb_diagnostics = models.ManyToManyField(
    #     verbose_name=('What TB diagnostic studies were performed? '),
    #     )
    #
    # tb_diagnostic_perf = models.CharField(
    #     verbose_name=('Were any of the TB diagnostic studies positive? '
    #     '□0= no □1= yes □2= pending □3= unable to determine Question 10: '
    #     'If yes, specify test and test result: (free text)'),)

    tb_diagnose_pos = models.CharField(
        verbose_name='Were any of the TB diagnostic studies positive',
        max_length=20,
        choices=YES_NO_UNABLE_DET,
        null=True,
        blank=True)

    tb_test_results = models.TextField(
        verbose_name='Specify test and test result',
        max_length=250,
        null=True,
        blank=True)

    tb_treat_start = models.CharField(
        verbose_name='Was TB treatment started?',
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True)

    tb_prev_therapy_start = models.CharField(
        verbose_name='Was TB preventative therapy started?',
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True)

    tb_comments = models.TextField(
        verbose_name='Comments',
        max_length=250,
        null=True,
        blank=True)

    class Meta:
        app_label = 'flourish_caregiver'
