from .model_mixins import CrfModelMixin, ReferralFUFormMixin


class CaregiverPhqReferralFU(ReferralFUFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'PHQ-9 Referral Follow Up Form for Caregivers'
        verbose_name_plural = 'PHQ-9 Referral Follow Up Form for Caregiver'
