from django.db import models
from edc_base.model_managers import HistoricalRecords
from .model_mixins import CaregiverContactFieldsMixin
from .subject_consent import SubjectConsent


class CaregiverContactManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(
            subject_identifier=subject_identifier)


class CaregiverContact(CaregiverContactFieldsMixin):
    consent_model = SubjectConsent

    call_reason_other = models.CharField(
        verbose_name='Other, specify',
        max_length=70,
        null=True,
        blank=True
    )

    contact_comment = models.TextField(
        verbose_name='Outcome of call',
        max_length=500,
        null=True,
        blank=True
    )
    study_name = models.CharField(
        verbose_name="Study name",
        max_length=20,
        default='flourish'
    )

    history = HistoricalRecords()

    objects = CaregiverContactManager()

    def natural_key(self):
        return (self.subject_identifier,)

    class Meta:
        app_label = 'flourish_caregiver'
        unique_together = ('subject_identifier', 'contact_datetime')
        verbose_name = 'Caregiver Contact'
