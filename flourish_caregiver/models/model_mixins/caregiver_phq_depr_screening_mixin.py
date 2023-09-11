from ...choices import DEPRESSION_SCALE
from django.db import models


class CaregiverPhqDeprScreeningMixin(models.Model):
    activity_interest = models.CharField(
        verbose_name='Little interest or pleasure in doing things',
        choices=DEPRESSION_SCALE,
        max_length=25, )

    depressed = models.CharField(
        verbose_name='Feeling down, depressed, or hopelesss',
        choices=DEPRESSION_SCALE,
        max_length=25, )

    sleep_disorders = models.CharField(
        verbose_name='Trouble falling/staying asleep, sleeping too much',
        choices=DEPRESSION_SCALE,
        max_length=25, )

    fatigued = models.CharField(
        verbose_name='Feeling tired or having little energy',
        choices=DEPRESSION_SCALE,
        max_length=25, )

    eating_disorders = models.CharField(
        verbose_name='Poor appetite or overeating',
        choices=DEPRESSION_SCALE,
        max_length=25, )

    self_doubt = models.CharField(
        verbose_name=('Feeling bad about yourself or that you are a failure or'
                      ' have let yourself or your family down'),
        choices=DEPRESSION_SCALE,
        max_length=25, )

    easily_distracted = models.CharField(
        verbose_name=('Trouble concentrating on things, such as reading the '
                      'newspaper or watching television.'),
        choices=DEPRESSION_SCALE,
        max_length=25, )

    restlessness = models.CharField(
        verbose_name=('Moving or speaking so slowly that other people could '
                      'have noticed. Or the opposite; being so fidgety or '
                      'restless that you have been moving around a lot more than usual'),
        choices=DEPRESSION_SCALE,
        max_length=25, )

    self_harm = models.CharField(
        verbose_name=('Thoughts that you would be better off dead or of '
                      'hurting yourself in some way'),
        choices=DEPRESSION_SCALE,
        max_length=25, )

    depression_score = models.IntegerField(
        verbose_name='Depression score',
        null=True,
        blank=True)

    class Meta:
        abstract = True
