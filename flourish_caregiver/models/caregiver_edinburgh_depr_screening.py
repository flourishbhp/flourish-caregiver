from django.db import models

from .model_mixins import CrfModelMixin

from ..choices import (ABLE_TO_LAUGH, ANXIOUS, CRYING, ENJOYMENT_TO_THINGS,
                       HARM, MISERABLE_FEELING, PANICK, SELF_BLAME,
                       SLEEPING_DIFFICULTY, TOP)

from .model_mixins import CaregiverEdinburghDeprScreeningMixin


class CaregiverEdinburghDeprScreening(CaregiverEdinburghDeprScreeningMixin, CrfModelMixin):

    def save(self, *args, **kwargs):
        self.depression_score = self.calculate_depression_score()
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Depression Screening – Edinburgh'
        verbose_name_plural = 'Depression Screening – Edinburgh'
