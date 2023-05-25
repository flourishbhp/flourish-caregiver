from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_protocol.validators import datetime_not_before_study_start

from .model_mixins import SearchSlugModelMixin


class CohortSchedules(SiteModelMixin,
                 SearchSlugModelMixin, BaseUuidModel):
    """ A model completed by the system for cohort assignment.
    """

    schedule_name = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Schedule name",
    )

    schedule_type = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Schedule name",
    )

    cohort_name = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Cohort name",
    )

    onschedule_model = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="OnSchedule model",
    )

    child_count = models.IntegerField(
        verbose_name="Child count",
    )

    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Cohort Schedule"
        verbose_name_plural = "Cohort Schedules"
        unique_together = ['cohort_name', 'schedule_type', 'child_count']
