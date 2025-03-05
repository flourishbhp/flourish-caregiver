from .model_mixins import CrfModelMixin, ReferralFormMixin


class HITSReferral(ReferralFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'HITS Referral'
