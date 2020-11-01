from django.db import models

from .model_mixins import CrfModelMixin
from ..choices import DEPRESSION_SCALE


class CaregiverGadAnxietyScreening(CrfModelMixin):

    feeling_anxious = models.CharField(
        verbose_name='Feeling nervous, anxious, or on edge',
        choices=DEPRESSION_SCALE,
        max_length=2)

    control_worrying = models.CharField(
        verbose_name='Not being able to stop or control worrying',
        choices=DEPRESSION_SCALE,
        max_length=2)

    worrying = models.CharField(
        verbose_name='Worrying too much about different things',
        choices=DEPRESSION_SCALE,
        max_length=2)

    trouble_relaxing = models.CharField(
        choices=DEPRESSION_SCALE,
        max_length=2)

    restlessness = models.CharField(
        verbose_name='Being so restless that it is hard to sit still',
        choices=DEPRESSION_SCALE,
        max_length=2)

    easily_annoyed = models.CharField(
        verbose_name='Becoming easily annoyed or irritable',
        choices=DEPRESSION_SCALE,
        max_length=2)

    fearful = models.CharField(
        verbose_name='Feeling afraid, as if something awful might happen',
        choices=DEPRESSION_SCALE,
        max_length=2)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Anxiety Screening - GAD-7'
        verbose_name_plural = 'Anxiety Screening - GAD-7'
