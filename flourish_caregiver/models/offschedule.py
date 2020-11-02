from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_identifier.managers import SubjectIdentifierManager

from edc_visit_schedule.model_mixins import OffScheduleModelMixin
from .model_mixins import ConsentVersionModelModelMixin


class MaternalOffSchedule(ConsentVersionModelModelMixin, OffScheduleModelMixin, BaseUuidModel):

    schedule_name = models.CharField(
        max_length=25,
        blank=True,
        null=True)

    objects = SubjectIdentifierManager()

    on_site = CurrentSiteManager()

    history = HistoricalRecords()

    def take_off_schedule(self):
        pass

    class Meta:
        unique_together = ('subject_identifier', 'schedule_name')
