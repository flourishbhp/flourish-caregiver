from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_protocol.validators import datetime_not_before_study_start

from flourish_caregiver.choices import REASONS_UNWILLING_ADOL


class TbAdolEligibility(NonUniqueSubjectIdentifierModelMixin,
                        SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, datetime_not_before_study_start],)

    tb_adol_participation = models.CharField(
        verbose_name=('Participant willing to do an Informed consent for the '
                      'TB Adolescent Study'),
        choices=YES_NO,
        max_length=10,
        help_text='Eligible for TB adolescent study if NO')

    reasons_unwilling_part = models.CharField(
        verbose_name='Reasons unable to obtain an informed consent for TB study',
        choices=REASONS_UNWILLING_ADOL,
        max_length=50,
        blank=True,
        null=True
    )

    reasons_unwilling_part_other = OtherCharField()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Adolescent Study Screening'
