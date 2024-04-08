from django.db import models
from flourish_caregiver.choices import CAREGIVER_OR_CHILD
from flourish_caregiver.models.list_models import CaregiverSocialWorkReferralList
from .model_mixins import CrfModelMixin
from .model_mixins import CaregiverSocialWorkReferralMixin


class CaregiverSocialWorkReferral(CrfModelMixin, CaregiverSocialWorkReferralMixin):
    """ PRN form was changed from social work referral to just referral form. Can not
        change model definitions because data is already captured. Changed verbose_name.
        Added: referral_location
    """

    referral_reason = models.ManyToManyField(
        CaregiverSocialWorkReferralList,
        verbose_name=('Please indicate reasons for the need for a '
                      'referral for the participant (select all that apply)'),
    )
    referral_for = models.CharField(
        verbose_name='Referral For ',
        max_length=10,
        choices=CAREGIVER_OR_CHILD,
        default='caregiver')

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Referral'
        verbose_name_plural = 'Caregiver Referral'
