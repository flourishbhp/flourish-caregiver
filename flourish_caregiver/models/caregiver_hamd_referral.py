from .model_mixins import CrfModelMixin, ReferralFormMixin


class CaregiverHamdReferral(ReferralFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver HAM-D Referral Form'
        verbose_name_plural = 'Caregiver HAM-D Referral Form'
