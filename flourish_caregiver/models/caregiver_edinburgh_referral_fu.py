from .model_mixins import CrfModelMixin, ReferralFUFormMixin


class CaregiverEdinburghReferralFU(ReferralFUFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Edinburgh Referral Follow Up Form'
        verbose_name_plural = 'Caregiver Edinburgh Referral Follow Up Form'
