from django.db import models
from edc_base.model_validators.date import date_not_future
from edc_constants.constants import YES
from edc_constants.choices import YES_NO

from flourish_caregiver.choices import YES_NO_UKN_CHOICES
from flourish_caregiver.models.list_models import TBTests
from flourish_child.choices import (DURATION_OPTIONS, TEST_RESULTS_CHOICES,
                                    YES_NO_DN_RECALL)


class TBScreeningMixin(models.Model):
    cough = models.CharField(
        verbose_name='Do you currently have any cough?',
        choices=YES_NO_UKN_CHOICES,
        max_length=20)

    cough_duration = models.CharField(
        verbose_name='How long has the cough lasted?',
        choices=DURATION_OPTIONS,
        max_length=10, blank=True, null=True)

    fever = models.CharField(
        verbose_name='Do you currently have a fever?',
        choices=YES_NO_UKN_CHOICES,
        max_length=20)

    fever_duration = models.CharField(
        verbose_name='How long has the fever lasted?',
        choices=DURATION_OPTIONS,
        max_length=10, blank=True, null=True)

    sweats = models.CharField(
        verbose_name='Are you currently experiencing night sweats?',
        choices=YES_NO_UKN_CHOICES,
        max_length=20)

    sweats_duration = models.CharField(
        verbose_name='How long have the night sweats lasted?',
        choices=DURATION_OPTIONS,
        max_length=10, blank=True, null=True)

    weight_loss = models.CharField(
        verbose_name='Since the last time you spoke with FLOURISH staff, have you had '
                     'any weight loss?',
        choices=YES_NO_UKN_CHOICES,
        max_length=20, )

    weight_loss_duration = models.CharField(
        verbose_name='How long has the weight loss lasted?',
        choices=DURATION_OPTIONS,
        max_length=10, blank=True, null=True)

    household_diagnosed_with_tb = models.CharField(
        verbose_name='Since the last time you spoke with FLOURISH staff, has someone in '
                     'your household been diagnosed with TB? ',
        choices=YES_NO_UKN_CHOICES,
        max_length=20, )

    evaluated_for_tb = models.CharField(
        verbose_name='Since the last time you spoke with FLOURISH staff, have you been '
                     'evaluated in a clinic for TB?',
        choices=YES_NO_UKN_CHOICES,
        default='',
        max_length=20, )

    clinic_visit_date = models.DateField(
        verbose_name='What was the date of the clinic visit?',
        validators=[date_not_future, ],
        blank=True, null=True)

    tb_tests = models.ManyToManyField(
        TBTests,
        blank=True,
        verbose_name='What diagnostic tests were performed for TB?',
        default='',)

    other_test = models.TextField(
        verbose_name='If "Other", specify test and result',
        blank=True,
        null=True)

    chest_xray_results = models.CharField(
        verbose_name='Chest Xray Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    sputum_sample_results = models.CharField(
        verbose_name='Sputum sample Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)
    
    urine_test_results = models.CharField(
        verbose_name='Urine Test Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    stool_sample_results = models.CharField(
        verbose_name='Stool sample Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    skin_test_results = models.CharField(
        verbose_name='Skin Test Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    blood_test_results = models.CharField(
        verbose_name='Blood Test Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    other_test_results = models.TextField(verbose_name='Other Test Result',
                                          blank=True,
                                          null=True)

    persistent_symptoms = models.CharField(
        verbose_name=('Were any symptoms (cough, fever, night sweats, '
                      'weight loss, or fatigue) present when you last '
                      'spoke with FLOURISH staff?'),
        choices=YES_NO_DN_RECALL,
        max_length=13)

    flourish_referral = models.CharField(
        verbose_name='Were you referred by our FLOURISH clinic team?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    tb_diagnoses = models.BooleanField(
        blank=True,
        null=True
    )

    @property
    def symptomatic(self):
        return (self.cough == YES or
                self.fever == YES or
                self.sweats == YES or
                self.weight_loss == YES)

    class Meta:
        abstract = True
