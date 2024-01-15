from django.db import models

from flourish_caregiver.choices import PARTNER_ACTIONS_CHOICES
from flourish_caregiver.models.model_mixins import CrfModelMixin


class HITSScreening(CrfModelMixin):
    physical_hurt = models.CharField(
        verbose_name='How often does your partner physically hurt you?',
        choices=PARTNER_ACTIONS_CHOICES,
        max_length=5)

    insults = models.CharField(
        verbose_name='How often does your partner insult or talk down to you?',
        choices=PARTNER_ACTIONS_CHOICES,
        max_length=5)

    threaten = models.CharField(
        verbose_name='How often does your partner threaten you with harm?',
        choices=PARTNER_ACTIONS_CHOICES,
        max_length=5)

    screem_curse = models.CharField(
        verbose_name='How often does your partner scream or curse at you?',
        choices=PARTNER_ACTIONS_CHOICES,
        max_length=5)

    score = models.IntegerField(
        verbose_name='Total HITS Score',
        default=0,
        blank=True,
        null=True,
        max_length=5)

    def save(self, *args, **kwargs):
        self.score = (int(self.physical_hurt) + int(self.insults) + int(self.threaten) +
                      int(self.screem_curse))
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'HITS Screening'
        verbose_name_plural = 'HITS Screenings'
