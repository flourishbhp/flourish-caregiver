from django.db import models
from flourish_caregiver.choices import CAREGIVER_OR_CHILD
from flourish_caregiver.models.list_models import CaregiverSocialWorkReferralList
from .model_mixins import CrfModelMixin
from .model_mixins import CaregiverSocialWorkReferralMixin


class CaregiverSocialWorkReferral(CrfModelMixin, CaregiverSocialWorkReferralMixin):

    referral_reason = models.ManyToManyField(
        CaregiverSocialWorkReferralList,
        verbose_name=('Please indicate reasons for the need for a social work '
                      'referral for the Mother/Caregiver or Child (select all that apply)'),
    )
    referral_for = models.CharField(
        verbose_name='Referral For ',
        max_length=10,
        choices=CAREGIVER_OR_CHILD,
        default='caregiver')

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Social Work Referral'
        verbose_name_plural = 'Caregiver Social Work Referral'
