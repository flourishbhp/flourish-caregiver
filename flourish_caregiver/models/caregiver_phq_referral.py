from .model_mixins import CrfModelMixin, ReferralFormMixin


class CaregiverPhqReferral(ReferralFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver PHQ-9 Referral Form'
        verbose_name_plural = 'Caregiver PHQ-9 Referral Form'
