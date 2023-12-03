from flourish_caregiver.models.model_mixins import CrfModelMixin
from flourish_caregiver.models.model_mixins.flourish_tb_referral_mixin import \
    TBReferralMixin


class TBReferralCaregiver(CrfModelMixin, TBReferralMixin):
    class Meta(TBReferralMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver TB Referral'
        verbose_name_plural = 'Caregiver TB Referrals'
