from .model_mixins import CrfModelMixin, ReferralFUFormMixin


class CaregiverHamdReferralFU(ReferralFUFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver HAM-D Referral Follow Up Form'
        verbose_name_plural = 'Caregiver HAM-D Referral Follow Up Form'
