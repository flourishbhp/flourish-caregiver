from django import forms
from django.apps import apps as django_apps
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_identifier.managers import SubjectIdentifierManager

from edc_visit_schedule.model_mixins import OffScheduleModelMixin


class CaregiverOffSchedule(OffScheduleModelMixin, BaseUuidModel):

    schedule_name = models.CharField(
        max_length=25,
        blank=True,
        null=True)

    objects = SubjectIdentifierManager()

    on_site = CurrentSiteManager()

    history = HistoricalRecords()

    def take_off_schedule(self):
        pass

    @property
    def latest_consent_obj_version(self):

        caregiver_consent_cls = django_apps.get_model('flourish_caregiver.subjectconsent')

        subject_consents = caregiver_consent_cls.objects.filter(
             subject_identifier=self.subject_identifier,)
        if subject_consents:
            latest_consent = subject_consents.latest('consent_datetime')
            return latest_consent.version
        else:
            raise forms.ValidationError('Missing Subject Consent form, cannot proceed.')

    def save(self, *args, **kwargs):
        self.consent_version = self.latest_consent_obj_version
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('subject_identifier', 'schedule_name')
