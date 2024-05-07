from django.db import models
from ...choices import (ABLE_TO_LAUGH, ANXIOUS, CRYING, ENJOYMENT_TO_THINGS,
                        HARM, MISERABLE_FEELING, PANICK, SELF_BLAME,
                        SLEEPING_DIFFICULTY, TOP)


class CaregiverEdinburghDeprScreeningMixin(models.Model):
    able_to_laugh = models.CharField(
        verbose_name='I have been able to laugh and see the funny '
                     'side of things',
        choices=ABLE_TO_LAUGH,
        max_length=2)

    enjoyment_to_things = models.CharField(
        verbose_name='I have looked forward with enjoyment of things',
        choices=ENJOYMENT_TO_THINGS,
        max_length=2)

    self_blame = models.CharField(
        verbose_name='I have blamed myself unnecessarily when '
                     'things went wrong',
        choices=SELF_BLAME,
        max_length=2)

    anxious = models.CharField(
        verbose_name='I have been anxious or worried for no good reason',
        choices=ANXIOUS,
        max_length=2)

    panicky = models.CharField(
        verbose_name='I have felt scared or panicky for no very good reason',
        choices=PANICK,
        max_length=20)

    coping = models.CharField(
        verbose_name='Things have been getting on top of me',
        choices=TOP,
        max_length=2)

    sleeping_difficulty = models.CharField(
        verbose_name='I have been so unhappy that I have had difficulty in sleeping',
        choices=SLEEPING_DIFFICULTY,
        max_length=2)

    miserable_feeling = models.CharField(
        verbose_name='I have felt sad or miserable',
        choices=MISERABLE_FEELING,
        max_length=2)

    unhappy = models.CharField(
        verbose_name='I have been so unhappy that I have been crying',
        choices=CRYING,
        max_length=20)

    self_harm = models.CharField(
        verbose_name='The thought of harming myself has occurred to me',
        choices=HARM,
        max_length=2)

    depression_score = models.IntegerField(
        verbose_name='Depression score',
        null=True,
        blank=True)

    def calculate_depression_score(self):
        score = 0
        for f in self._meta.get_fields():
            if f.name in ['able_to_laugh', 'enjoyment_to_things', 'self_blame',
                          'anxious', 'panicky', 'coping', 'sleeping_difficulty',
                          'miserable_feeling', 'unhappy', 'self_harm', ]:
                score += int(getattr(self, f.name))
        return score

    class Meta:
        abstract = True
