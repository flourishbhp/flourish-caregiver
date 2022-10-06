from django.core.validators import MaxValueValidator
from django.db import models
from ..choices import INTERVIEW_LOCATIONS
from .model_mixins import CrfModelMixin


class TbInterview(CrfModelMixin):

    interview_location = models.CharField(
        verbose_name='Location of the interview',
        choices=INTERVIEW_LOCATIONS,
        max_length=100)

    interview_location_other = models.TextField(
        verbose_name='If other, specify ',
        max_length=100,
        null=True,
        blank=True)

    interview_duration = models.PositiveIntegerField(
        verbose_name='Duration of interview:',
        validators=[MaxValueValidator(1440), ],
        help_text='Insert number of minutes')

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Interview'
