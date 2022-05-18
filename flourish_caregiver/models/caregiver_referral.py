from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_action_item.model_mixins import ActionModelMixin
from edc_base.model_validators.date import datetime_not_future
from edc_protocol.validators import datetime_not_before_study_start
from edc_constants.choices import YES_NO
from ..choices import POS_NEG_IND
from edc_base.utils import get_utcnow
from .list_models import CaregiverReferralReasons
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from .model_mixins import CrfModelMixin


class CaregiverReferral(CrfModelMixin):
    
    """Updates
    -caregiver visit
    -date of completion
    -is participant currently pregnancy
    -HIV status
    -Please indicate reasons for the need for a social work referral for the Mother/Caregiver (select all that apply)
    -comment
    """
    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use'
                   ' the date/time this information was reported.'))
    
    is_pregnant = models.CharField(
        verbose_name="Was a pregnancy test performed?",
        max_length=3,
        choices=YES_NO,
    )
    
    hiv_status = models.CharField(
        verbose_name='What is the HIV status?',
        choices=POS_NEG_IND,
        max_length=15,
        blank=True,
        null=True)
    
    referral_reason = models.ManyToManyField(
        CaregiverReferralReasons,
        verbose_name=('Please indicate reasons for the need for a'
                      'social work referral for the Mother/Caregiver (select all that apply)'),
        blank=True
    )
    
    referred_other = OtherCharField()
    
    comment = models.TextField(
        verbose_name='Comment',
        blank=True,
        null=True)   
     
    
    history = HistoricalRecords()
    
    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Maternal Referral'
        verbose_name_plural = 'Maternal Referral'
    
    
    
    
    