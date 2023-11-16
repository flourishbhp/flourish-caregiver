from django.db import models

from .model_mixins import CrfModelMixin
from .model_mixins import CaregiverSocialWorkReferralMixin
from .list_models import CaregiverSocialWorkReferralList


class CaregiverSocialWorkReferral(CrfModelMixin, CaregiverSocialWorkReferralMixin):
    
    referral_reason = models.ManyToManyField(
        CaregiverSocialWorkReferralList,
        verbose_name=('Please indicate reasons for the need for a social work '
                      'referral for the Mother/Caregiver or Child (select all that apply)'),
        blank=True
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Social Work Referral'
        verbose_name_plural = 'Caregiver Social Work Referral'
