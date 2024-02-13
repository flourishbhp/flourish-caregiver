from .model_mixins import CaregiverGadAnxietyScreeningMixin
from .model_mixins import CrfModelMixin


class CaregiverGadAnxietyScreening(CaregiverGadAnxietyScreeningMixin, CrfModelMixin):

    def save(self, *args, **kwargs):
        self.anxiety_score = self.calculate_depression_score
        super().save(*args, **kwargs)

    @property
    def calculate_depression_score(self):
        score = 0
        for f in self._meta.get_fields():
            if f.name in ['feeling_anxious', 'control_worrying', 'worrying',
                          'trouble_relaxing', 'restlessness', 'easily_annoyed',
                          'fearful', ]:
                score += int(getattr(self, f.name))
        return score

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Anxiety Screening - GAD-7'
        verbose_name_plural = 'Anxiety Screening - GAD-7'
