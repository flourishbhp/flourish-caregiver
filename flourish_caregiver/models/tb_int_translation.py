from django.db import models
from .model_mixins import CrfModelMixin


class TbInterviewTranslation(CrfModelMixin):

    translation_date = models.DateField(
        verbose_name='Date translation completed')

    translator = models.CharField(
         verbose_name='Name of staff who performed translation',
         max_length=30)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Translation'
