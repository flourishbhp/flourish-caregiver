from django.core.validators import MaxValueValidator
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
        validators=[MaxValueValidator(1440), ],
        help_text='Insert number of minutes')

    # # mp3 upload field
    interview_file = models.FileField(upload_to='tb_int/', null=True)

    interview_language = models.CharField(
        verbose_name='In what language was the interview performed? ',
        choices=INTERVIEW_LANGUAGE,
        max_length=10)

    translation_date = models.DateField(
        verbose_name='Date translation completed',
        null=True,
        blank=True)

    translator_name = models.CharField(
        verbose_name='Name of staff who performed translation',
        max_length=30,
        blank=True,
        null=True)

    interview_translation = models.FileField(upload_to='tb_int/docs/', null=True)

    transcription_date = models.DateField(
        verbose_name='Date transcription completed',
        null=True,
        blank=True)

    transcriber_name = models.CharField(
        verbose_name='Name of staff who performed transcription',
        max_length=30,
        blank=True,
        null=True)

    interview_transcription = models.FileField(upload_to='tb_int/docs/', null=True)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Interview'
