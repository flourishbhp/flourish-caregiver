from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin

from .model_mixins import SearchSlugModelMixin


class CohortSchedules(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):
    """ A model completed by the system for cohort assignment.
    """

    schedule_name = models.CharField(
        max_length=50,
        verbose_name="Schedule name",
    )

    schedule_type = models.CharField(
        max_length=50,
        verbose_name="Schedule type",
    )

    cohort_name = models.CharField(
        max_length=50,
        verbose_name="Cohort name",
    )

    onschedule_model = models.CharField(
        max_length=100,
        verbose_name="OnSchedule model",
    )

    child_count = models.IntegerField(
        verbose_name="Child count",
        null=True
    )

    def get_search_slug_fields(self):
        fields = ['schedule_name']
        return fields

    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Cohort Schedule"
        verbose_name_plural = "Cohort Schedules"
