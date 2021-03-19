from .model_mixins import CrfModelMixin, ReferralFormMixin


class CaregiverEdinburghReferral(ReferralFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Edinburgh Referral Form'
        verbose_name_plural = 'Caregiver Edinburgh Referral Form'
