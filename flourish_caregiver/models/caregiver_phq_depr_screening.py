from .model_mixins import CaregiverPhqDeprScreeningMixin
from .model_mixins import CrfModelMixin


class CaregiverPhqDeprScreening(CaregiverPhqDeprScreeningMixin, CrfModelMixin):

    def save(self, *args, **kwargs):
        self.depression_score = self.calculate_depression_score()
        super().save(*args, **kwargs)

    def calculate_depression_score(self):
        score = 0
        for f in self._meta.get_fields():
            if f.name in ['activity_interest', 'depressed', 'sleep_disorders',
                          'fatigued', 'eating_disorders', 'self_doubt',
                          'easily_distracted', 'restlessness', 'self_harm', ]:
                score += int(getattr(self, f.name))
        return score

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Depression Screening - PHQ-9'
        verbose_name_plural = 'Depression Screening - PHQ-9'
