from .model_mixins import CaregiverEdinburghDeprScreeningMixin
from .model_mixins import CrfModelMixin


class CaregiverEdinburghDeprScreening(CaregiverEdinburghDeprScreeningMixin,
                                      CrfModelMixin):

    def save(self, *args, **kwargs):
        self.depression_score = self.calculate_depression_score()
        super().save(*args, **kwargs)

    def calculate_depression_score(self):
        score = 0
        for f in self._meta.get_fields():
            if f.name in ['able_to_laugh', 'enjoyment_to_things', 'self_blame',
                          'anxious', 'panicky', 'coping', 'sleeping_difficulty',
                          'miserable_feeling', 'unhappy', 'self_harm', ]:
                score += int(getattr(self, f.name))
        return score

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Depression Screening – Edinburgh'
        verbose_name_plural = 'Depression Screening – Edinburgh'
