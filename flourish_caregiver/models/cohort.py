from django.apps import apps as django_apps
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
from .caregiver_child_consent import CaregiverChildConsent
from ..helper_classes import MaternalStatusHelper
from ..helper_classes.schedule_dict import child_schedule_dict


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

    @property
    def schedule_history_cls(self):
        return django_apps.get_model('edc_visit_schedule.subjectschedulehistory')

    @property
    def check_exposure(self):
        child_consent = CaregiverChildConsent.objects.filter(
            subject_identifier=self.subject_identifier).first()
        maternal_status = MaternalStatusHelper(subject_identifier=self.subject_identifier)
        child_dataset = getattr(child_consent, 'child_dataset', None)
        if child_dataset:
            return getattr(child_dataset, 'infant_hiv_exposed', None).upper()
        else:
            hiv_status = getattr(maternal_status, 'hiv_status', None)
            return f'ANC_{hiv_status}'

    @property
    def check_onschedule(self):
        cohort_onschedules = [name_dict.get('name') for name_dict in child_schedule_dict.get(self.name).values()]
        onschedules = self.schedule_history_cls.objects.onschedules(
            subject_identifier=self.subject_identifier)
        onschedules = [onsch for onsch in onschedules if onsch.schedule_name in cohort_onschedules]
        return bool(onschedules)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Cohort"
        verbose_name_plural = "Cohort"
        unique_together = ('subject_identifier', 'name')
