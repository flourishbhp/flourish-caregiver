from .model_mixins import CrfModelMixin
from .model_mixins import CaregiverSocialWorkReferralMixin


class CaregiverSocialWorkReferral(CrfModelMixin, CaregiverSocialWorkReferralMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Social Work Referral'
        verbose_name_plural = 'Caregiver Social Work Referral'
