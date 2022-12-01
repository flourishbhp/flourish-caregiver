from .model_mixins import CrfModelMixin, ReferralFUFormMixin


class CaregiverEdinburghPostReferral(ReferralFUFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Edinburgh Post Referral Form'
        verbose_name_plural = 'Caregiver Edinburgh Post Referral Forms'
