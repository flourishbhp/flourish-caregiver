from .model_mixins import CrfModelMixin, ReferralFormMixin


class CaregiverPhqReferral(ReferralFormMixin, CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
<<<<<<< HEAD
        verbose_name = 'PHQ-9 Referral Form for Caregivers'
        verbose_name_plural = 'Caregiver Referral'
=======
        verbose_name = 'Caregiver PHQ-9 Referral Form'
        verbose_name_plural = 'Caregiver PHQ-9 Referral Form'
>>>>>>> 10658e898b7115019c711a2fe54810d3c80a8eb5
