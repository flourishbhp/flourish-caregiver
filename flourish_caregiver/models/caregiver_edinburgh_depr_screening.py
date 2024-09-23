from .model_mixins import CaregiverEdinburghDeprScreeningMixin
from .model_mixins import CrfModelMixin


class CaregiverEdinburghDeprScreening(CaregiverEdinburghDeprScreeningMixin,
                                      CrfModelMixin):

    def save(self, *args, **kwargs):
        self.depression_score = self.calculate_depression_score()
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Depression Screening – Edinburgh'
        verbose_name_plural = 'Depression Screening – Edinburgh'
