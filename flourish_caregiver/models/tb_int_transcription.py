from django.db import models
from .model_mixins import CrfModelMixin


class TbInterviewTranscription(CrfModelMixin):

    transcription_date = models.DateField(
        verbose_name='Date transcription completed')

    translator = models.CharField(
         verbose_name='Name of staff who performed transcription',
         max_length=30)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Transcription'
