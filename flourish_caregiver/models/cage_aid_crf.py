from .model_mixins import CrfModelMixin
from .model_mixins import CageAidFieldsMixin


class CaregiverCageAid(CrfModelMixin, CageAidFieldsMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = "CAGE-AID Substance Abuse Screening "
        verbose_name_plural = "CAGE-AID Substance Abuse Screening "
