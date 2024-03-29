from .model_mixins import CrfModelMixin, ReferralFUFormMixin


class CaregiverHamdPostReferral(ReferralFUFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver HAM-D Post Referral Form'
        verbose_name_plural = 'Caregiver HAM-D Post Referral Forms'
