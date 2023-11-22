from flourish_caregiver.models.model_mixins.crf_model_mixin import CrfModelMixin
from flourish_caregiver.models.model_mixins.flourish_tb_referral_outcome_mixin import \
    FlourishTbReferralOutcomeMixin


class CaregiverTBReferralOutcome(FlourishTbReferralOutcomeMixin, CrfModelMixin):
    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver TB Referral Outcomes CRF'
        verbose_name_plural = 'Caregiver TB Referral Outcomes CRFs'
