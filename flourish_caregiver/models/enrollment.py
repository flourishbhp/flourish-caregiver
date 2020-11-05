from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start

from .model_mixins import SearchSlugModelMixin


class Enrollment(NonUniqueSubjectIdentifierFieldMixin, SiteModelMixin,
                 SearchSlugModelMixin, BaseUuidModel):
    """ A model completed by the user for enrollment
    """

    enrollment_identifier = models.CharField(
        verbose_name='Enrollment Identifier',
        max_length=36,
        blank=True,
        null=True,
        unique=True)

    report_datetime = models.DateTimeField(
        verbose_name='Report Date and Time',
        default=get_utcnow,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        help_text='Date and time of enrollment')
    
    pregnant = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Are you currently pregnant?",
    )
    
    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollment"
