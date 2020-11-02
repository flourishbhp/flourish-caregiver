from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_identifier.managers import SubjectIdentifierManager

from edc_visit_schedule.model_mixins import OnScheduleModelMixin

from .model_mixins import ConsentVersionModelModelMixin


class OnScheduleAntenatalEnrollment(ConsentVersionModelModelMixin,
                                    OnScheduleModelMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by subject_consent.
    """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    schedule_name = models.CharField(max_length=25,
                                     blank=True,
                                     null=True)

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def put_on_schedule(self):
        pass

    class Meta:
        unique_together = ('subject_identifier', 'schedule_name')
