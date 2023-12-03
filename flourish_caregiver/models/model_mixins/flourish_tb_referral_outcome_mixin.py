from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from flourish_caregiver.choices import CLINIC_NAMES, TB_REASON_CHOICES
from flourish_caregiver.models.list_models import TBTests
from flourish_child.choices import TB_TREATMENT_CHOICES, TEST_RESULTS_CHOICES, \
    YES_NO_OTHER


class FlourishTbReferralOutcomeMixin(models.Model):
    tb_evaluation = models.CharField(
        verbose_name='Did participant go to clinic for TB evaluation?',
        choices=YES_NO,
        max_length=3)

    clinic_name = models.CharField(
        verbose_name='Clinic name for referral',
        choices=CLINIC_NAMES,
        max_length=20,
        blank=True, null=True)

    clinic_name_other = OtherCharField()

    tests_performed = models.ManyToManyField(
        TBTests,
        verbose_name='What diagnostic tests were performed for TB',
        blank=True, )

    other_test_specify = models.TextField(
        verbose_name='If "Other", specify',
        blank=True, null=True)

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

    skin_test_results = models.CharField(
        verbose_name='Skin Test Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    blood_test_results = models.CharField(
        verbose_name='Blood Test Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    other_test_results = models.CharField(
        verbose_name='Other Test Result',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    diagnosed_with_tb = models.CharField(
        verbose_name='Were you diagnosed with TB?',
        choices=YES_NO,
        max_length=3, blank=True, null=True)

    tb_treatment = models.CharField(
        verbose_name='Were you started on TB treatment?',
        choices=TB_TREATMENT_CHOICES,
        max_length=20, blank=True, null=True)

    other_tb_treatment = OtherCharField()

    tb_preventative_therapy = models.CharField(
        verbose_name='Were you started on TB preventative therapy?treatment (consists of '
                     'four or more drugs taken over several months)',
        choices=YES_NO_OTHER,
        max_length=10, blank=True, null=True)

    other_tb_preventative_therapy = OtherCharField()

    tb_isoniazid_preventative_therapy = models.CharField(
        verbose_name='Were you started on TB preventative therapy (such as isoniazid or '
                     'rifapentine/isoniazid for several months)? ',
        choices=YES_NO_OTHER,
        max_length=10, blank=True, null=True)

    other_tb_isoniazid_preventative_therapy = OtherCharField()

    reasons = models.CharField(
        verbose_name='Reasons not able to go to TB clinic for evaluation',
        choices=TB_REASON_CHOICES,
        max_length=30, blank=True, null=True)

    other_reasons = OtherCharField()

    class Meta:
        abstract = True
