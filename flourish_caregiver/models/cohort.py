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
    # For example cohort_a, cohort_b etc
    cohort = models.CharField(
        max_length=10,
        verbose_name="Cohort",
    )

    # For example followup, quartly, enrollment
    name = models.CharField(
        max_length=10,
        verbose_name="Name",
    )

    # For example a_enrol1_schedule1, etc
    schedule_name = models.CharField(
        max_length=20,
        verbose_name="Schedule Name",
    )

    # onschedule model used
    onschedule_model = models.CharField(
        max_length=20,
        verbose_name="On Schedule Model",
    )

    # date put on schedule
    assign_datetime = models.DateTimeField(
        verbose_name='Date put Onschedule',
        default=get_utcnow,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        help_text='Date and time for cohort assignment')

    onschedule_model = models.BooleanField(
        verbose_name="Currently on schedule",
        default=True,
        editable=False)

    enrollment_cohort = models.BooleanField(
        verbose_name="Study enrolment cohort",
        default=False,
        editable=False)

    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Cohort"
        verbose_name_plural = "Cohort"
