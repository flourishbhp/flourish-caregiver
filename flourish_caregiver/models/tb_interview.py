
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ..choices import INTERVIEW_LOCATIONS, INTERVIEW_LANGUAGE
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
        validators=[MinValueValidator(10), MaxValueValidator(1440)],
        help_text='Insert number of minutes')

    # # mp3 upload field
    interview_file = models.FileField(
        upload_to='tb_int/',
        validators=[FileExtensionValidator(['mp3'])],
        null=True)

    interview_language = models.CharField(
        verbose_name='In what language was the interview performed? ',
        choices=INTERVIEW_LANGUAGE,
        max_length=10)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Interview'
