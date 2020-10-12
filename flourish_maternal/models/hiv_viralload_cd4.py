from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_constants.choices import YES_NO

from ..maternal_choices import SIZE_CHECK


class HivViralLoadAndCd4(SiteModelMixin, BaseUuidModel):

    last_cd4_count_known = models.CharField(
        verbose_name='Is the caregiver’s last CD4 count known?',
        choices=YES_NO,
        max_length=3, )

    cd4_count = models.IntegerField(
        verbose_name='What is the caregiver’s CD4 count?',
        validators=[MinValueValidator(1), MaxValueValidator(9999)], )

    cd4_count_date = models.DateField(
        verbose_name='Date of CD4 count', )

    last_vl_known = models.CharField(
        verbose_name='Is the caregiver’s last viral load known?',
        choices=YES_NO,
        max_length=3, )

    vl_detectable = models.CharField(
        verbose_name='Was the viral load detectable?',
        choices=YES_NO,
        max_length=3, )

    recent_vl_results = models.IntegerField(
        verbose_name='Quantitative results of most recent Viral Load test',
        validators=[MinValueValidator(10), MaxValueValidator(150000)],
        help_text='copies/ml', )

    hiv_results_quantifier = models.CharField(
        choices=SIZE_CHECK,
        max_length=12, )

    last_vl_date = models.DateField(
        verbose_name='Date of last viral load test', )

    class Meta:
        app_label = 'flourish_maternal'
        verbose_name = 'HIV Viral Load and CD4'
        verbose_name_plural = 'HIV Viral Load and CD4'
