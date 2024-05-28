from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_constants.choices import YES_NO
from edc_base.model_fields import OtherCharField

from ..maternal_choices import CALL_REASON, REASONS_FOR_RESCHEDULING, OUTCOME_CALL
from .model_mixins import CaregiverContactFieldsMixin
from .subject_consent import SubjectConsent


class CaregiverContactManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(
            subject_identifier=subject_identifier)


class CaregiverContact(CaregiverContactFieldsMixin):
    consent_model = SubjectConsent

    call_reason = models.CharField(
        verbose_name='Reason for call',
        max_length=30,
        choices=CALL_REASON,
    )

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

    call_rescheduled = models.CharField(
        verbose_name='Was the visit rescheduled',
        max_length=10,
        choices=YES_NO,
        null=True,
        blank=True
    )

    reason_rescheduled = models.CharField(
        verbose_name='Please indicate reason for re-scheduling',
        max_length=50,
        choices=REASONS_FOR_RESCHEDULING,
        null=True,
        blank=True
    )
    reason_rescheduled_other = OtherCharField(
        max_length=255
    )

    call_outcome = models.CharField(
        verbose_name='Outcome of a phone call or Home visit',
        max_length=30,
        choices=OUTCOME_CALL)

    call_outcome_other = OtherCharField(
        max_length=255
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
