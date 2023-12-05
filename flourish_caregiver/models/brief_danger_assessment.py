from django.db import models
from edc_base.model_fields import IsDateEstimatedField
from edc_constants.choices import YES_NO

from flourish_caregiver.models.model_mixins import CrfModelMixin
from ..choices import YES_NO_INT_CHOICES


class BriefDangerAssessment(CrfModelMixin):
    physical_violence_increased = models.CharField(
        verbose_name='Has the physical violence increased in frequency over the past '
                     'year?',
        choices=YES_NO_INT_CHOICES,
        max_length=5)

    used_weapons = models.CharField(
        verbose_name='Has your partner ever used a weapon against you or threatened you '
                     'with a weapon?',
        choices=YES_NO_INT_CHOICES,
        max_length=5)

    capable_of_killing = models.CharField(
        verbose_name='Do you believe your partner is capable of killing you?',
        choices=YES_NO_INT_CHOICES,
        max_length=5)

    choke = models.CharField(
        verbose_name='Has your partner ever tried to choke you?',
        choices=YES_NO_INT_CHOICES,
        max_length=5)

    partner_violently = models.CharField(
        verbose_name='Is your partner violently and constantly jealous of you?',
        choices=YES_NO_INT_CHOICES,
        max_length=5)

    child_been_physically_hurt = models.CharField(
        verbose_name='Has your child been physically hurt by your partner?',
        choices=YES_NO,
        max_length=5)

    last_time_child_hurt_datetime = models.DateField(
        verbose_name='If yes, when was the last time this happened?',
        max_length=25,
        blank=True,
        null=True)

    last_time_child_hurt_estimated = IsDateEstimatedField(
        verbose_name="Is this date estimated?",
        null=True,
        blank=True)

    fear_partner_hurt_child = models.CharField(
        verbose_name='Do you fear your partner might physically hurt your child?',
        choices=YES_NO,
        max_length=5, )

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Brief Danger Assessment'
        verbose_name_plural = 'Brief Danger Assessments'
