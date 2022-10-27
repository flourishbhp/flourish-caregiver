
from .model_mixins import CrfModelMixin, ReferralFormMixin


class CaregiverGadReferral(ReferralFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver GAD-7 Referral Form'
        verbose_name_plural = 'Caregiver GAD-7 Referral Form'
