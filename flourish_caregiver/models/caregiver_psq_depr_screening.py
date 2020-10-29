from django.db import models

from flourish_caregiver import CrfModelMixin
from flourish_caregiver import DEPRESSION_SCALE


class CaregiverPsqDeprScreening(CrfModelMixin):

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
        default="",
        null=True,
        blank=True)

    def save(self, *args, **kwargs):
        self.depression_score = self.calculate_depression_score()
        super().save(*args, **kwargs)

    def calculate_depression_score(self):
        score = 0
        for f in self._meta.get_fields():
            if f.name in ['activity_interest', 'depressed', 'sleep_disorders',
                          'fatigued', 'eating_disorders', 'self_doubt', 'easily_distracted',
                          'restlessness', 'self_harm', ]:
                score += int(getattr(self, f.name))
        return score

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Depression Screening - PSQ-9'
        verbose_name_plural = 'Depression Screening - PSQ-9'
