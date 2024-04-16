from django.apps import apps as django_apps
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_constants.constants import NEG, POS
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start

from .caregiver_child_consent import CaregiverChildConsent
from .model_mixins import MatrixMatchVariablesMixin, SearchSlugModelMixin
from ..helper_classes import MaternalStatusHelper
from ..helper_classes.schedule_dict import child_schedule_dict


class Cohort(MatrixMatchVariablesMixin,
             NonUniqueSubjectIdentifierFieldMixin,
             SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):
    """ A model completed by the system for cohort assignment.
    """

    name = models.CharField(
        max_length=150,
        choices=YES_NO,
        verbose_name='Cohort name',
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

    current_cohort = models.BooleanField(
        verbose_name='Current cohort', )

    exposure_status = models.CharField(
        verbose_name='Exposure status (i.e. HIV exposed/unexposed',
        max_length=9, )

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.exposure_status = self.check_exposure()
        self.current_cohort = self.check_current_cohort()
        super().save(*args, **kwargs)

    @property
    def schedule_history_cls(self):
        return django_apps.get_model('edc_visit_schedule.subjectschedulehistory')

    @property
    def caregiver_child_consent(self):
        return CaregiverChildConsent.objects.filter(
            subject_identifier=self.subject_identifier).first()

    @property
    def caregiver_subject_identifier(self):
        return self.caregiver_child_consent.subject_consent.subject_identifier

    @property
    def screening_identifier(self):
        return self.caregiver_child_consent.subject_consent.screening_identifier

    def check_antenetal_exists(self):
        antenatal_cls = django_apps.get_model(
            'flourish_caregiver.antenatalenrollment')
        antenatal = antenatal_cls.objects.filter(
            subject_identifier=self.caregiver_subject_identifier)
        return antenatal.exists()

    def check_exposure(self):
        exposure = {POS: 'EXPOSED', NEG: 'UNEXPOSED', }
        child_dataset = getattr(self.caregiver_child_consent, 'child_dataset', None)
        if child_dataset:
            return getattr(child_dataset, 'infant_hiv_exposed', None).upper()
        else:
            maternal_status = MaternalStatusHelper(
                subject_identifier=self.caregiver_subject_identifier).hiv_status
            return exposure.get(maternal_status, maternal_status)

    def check_current_cohort(self):
        cohort_onschedules = [name_dict.get('name') for name_dict in
                              child_schedule_dict.get(self.name).values()]

        ignore_schedule = ['tb_adol', 'child_bu', 'facet']
        try:
            latest_onschedule = self.schedule_history_cls.objects.filter(
                subject_identifier=self.subject_identifier, ).exclude(
                schedule_name__in=ignore_schedule).latest(
                'onschedule_datetime', 'created')
        except self.schedule_history_cls.DoesNotExist:
            return self.check_antenetal_exists()
        else:
            return getattr(latest_onschedule, 'schedule_name', None) in cohort_onschedules

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Cohort'
        verbose_name_plural = 'Cohort'
        unique_together = ('subject_identifier', 'name')
