from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_protocol.validators import datetime_not_before_study_start

from ...choices import CAREGIVER_OR_CHILD, HIV_EXPOSURE_STATUS, HIV_STATUS, REFERRAL_LOCATION


class CaregiverSocialWorkReferralMixin(models.Model):
    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, datetime_not_before_study_start],)

    referral_for = models.CharField(
        verbose_name='Referral For ',
        max_length=10,
        choices=CAREGIVER_OR_CHILD)

    is_preg = models.CharField(
        verbose_name='Is this participant currently pregnant? ',
        max_length=3,
        choices=YES_NO,
        default=NO)

    current_hiv_status = models.CharField(
        verbose_name='Current HIV status?',
        choices=HIV_STATUS,
        max_length=14,
        blank=True,
        null=True)

    child_exposure_status = models.CharField(
        verbose_name='HIV exposure status',
        choices=HIV_EXPOSURE_STATUS,
        max_length=3,
        blank=True,
        null=True
    )

    reason_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    comment = models.TextField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        null=True)

    referral_loc = models.CharField(
        verbose_name='Please indicate the referral location',
        max_length=50,
        choices=REFERRAL_LOCATION,
        default='hospital_based_sw')

    referral_loc_other = OtherCharField()

    class Meta:
        abstract = True
