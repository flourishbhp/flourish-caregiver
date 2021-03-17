from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_identifier.managers import SubjectIdentifierManager

from edc_visit_schedule.model_mixins import OnScheduleModelMixin as BaseOnScheduleModelMixin


class OnScheduleModelMixin(BaseOnScheduleModelMixin, BaseUuidModel):
    """A model used by the system. Auto-completed by enrollment model.
    """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    schedule_name = models.CharField(max_length=25, blank=True, null=True)

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def put_on_schedule(self):
        pass

    def save(self, *args, **kwargs):
        self.consent_version = '1'
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('subject_identifier', 'schedule_name')
        abstract = True


class OnScheduleCohortA1(OnScheduleModelMixin):
    pass


class OnScheduleCohortA2(OnScheduleModelMixin):
    pass


class OnScheduleCohortA3(OnScheduleModelMixin):
    pass


class OnScheduleCohortB1(OnScheduleModelMixin):
    pass


class OnScheduleCohortB2(OnScheduleModelMixin):
    pass


class OnScheduleCohortB3(OnScheduleModelMixin):
    pass


class OnScheduleCohortC1(OnScheduleModelMixin):

    pass


class OnScheduleCohortC2(OnScheduleModelMixin):

    pass


class OnScheduleCohortC3(OnScheduleModelMixin):

    pass


class OnSchedulePool1(OnScheduleModelMixin):

    pass


class OnSchedulePool2(OnScheduleModelMixin):

    pass


class OnSchedulePool3(OnScheduleModelMixin):

    pass
