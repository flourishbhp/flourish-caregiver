from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_protocol.validators import datetime_not_before_study_start
from edc_visit_schedule.models import SubjectScheduleHistory
from .model_mixins import SearchSlugModelMixin


class CohortSchedules(SubjectScheduleHistory):
    """ A model completed by the system for cohort assignment.
    """
