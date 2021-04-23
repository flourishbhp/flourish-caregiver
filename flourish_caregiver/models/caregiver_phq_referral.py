from .model_mixins import CrfModelMixin, ReferralFormMixin


class CaregiverPhqReferral(ReferralFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'PHQ-9 Referral Form for Caregivers'
        verbose_name_plural = 'PHQ-9 Referral Form for Caregiver'
