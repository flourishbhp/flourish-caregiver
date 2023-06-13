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


class Cohort(NonUniqueSubjectIdentifierFieldMixin, SiteModelMixin,
                 SearchSlugModelMixin, BaseUuidModel):
    """ A model completed by the system for cohort assignment.
    """

    name = models.CharField(
        max_length=150,
        choices=YES_NO,
        verbose_name="Cohort name",
    )

    assign_datetime = models.DateTimeField(
        verbose_name='Report Date and Time',
        default=get_utcnow,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        help_text='Date and time for cohort assignment')

    enrollment_cohort = models.BooleanField(
        verbose_name="Study enrolment cohort",
        default=False,
        editable=False)

    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Cohort"
        verbose_name_plural = "Cohort"
