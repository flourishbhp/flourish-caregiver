from .model_mixins import CrfModelMixin, ReferralFUFormMixin


class CaregiverGadReferralFU(ReferralFUFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver GAD-7 Referral Follow Up Form'
        verbose_name_plural = 'Caregiver GAD-7 Referral Follow Up Form'
