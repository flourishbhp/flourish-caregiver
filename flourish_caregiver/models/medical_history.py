from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO, YES_NO_NA

from .list_models import CaregiverMedications, ChronicConditions, GeneralSymptoms, \
    WcsDxAdult
from .model_mixins import CrfModelMixin
from ..choices import CLINIC_VISIT_CHOICES
from ..maternal_choices import KNOW_HIV_STATUS


class MedicalHistory(CrfModelMixin):
    """A model completed by the user on Medical History for all care givers."""

    chronic_since = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name='Does the caregiver have any chronic conditions?', )

    caregiver_chronic = models.ManyToManyField(
        ChronicConditions,
        related_name='caregiver',
        verbose_name=('Does the caregiver have any of the above. Tick all '
                      'that apply'),
    )

    caregiver_chronic_other = OtherCharField(
        max_length=35,
        verbose_name='If other, specify.',
        blank=True,
        null=True)

    who_diagnosis = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        verbose_name=('Has the caregiver ever been diagnosed with a WHO Stage'
                      ' III or IV illness?'),
        help_text=('Please use the WHO Staging Guidelines. ONLY for HIV '
                   'infected caregivers')
    )

    who = models.ManyToManyField(
        WcsDxAdult,
        verbose_name='List any new WHO Stage III/IV diagnoses that are '
                     'not reported'
    )

    who_other = OtherCharField(
        max_length=35,
        verbose_name='If other, specify.',
        blank=True,
        null=True)

    caregiver_medications = models.ManyToManyField(
        CaregiverMedications,
        verbose_name='Does the caregiver currently take any of the above '
                     'medications. Tick all that apply',
        blank=True
    )

    caregiver_medications_other = OtherCharField(
        max_length=35,
        verbose_name='If other, specify.',
        blank=True,
        null=True)

    know_hiv_status = models.CharField(
        max_length=50,
        verbose_name='How many people know that you are living with HIV?',
        choices=KNOW_HIV_STATUS)

    comment = models.TextField(
        max_length=250,
        verbose_name='Comments',
        blank=True,
        null=True)

    """Quartely phone calls stem question"""
    med_history_changed = models.CharField(
        verbose_name='Has any of your following medical history changed?',
        max_length=3,
        choices=YES_NO,
        null=True)

    # Version 2 changes

    current_illness = models.CharField(
        verbose_name="Do you have any current illness?",
        max_length=10,
        choices=YES_NO
    )

    current_symptoms = models.ManyToManyField(
        GeneralSymptoms,
        verbose_name="What are your current symptoms",
        blank=True,
        related_name='mmaternal_current_symptoms'
    )

    current_symptoms_other = models.TextField(
        verbose_name='If other, specify.',
        blank=True,
        null=True)

    symptoms_start_date = models.DateField(
        verbose_name="When did the symptoms start.",
        validators=[date_not_future],
        null=True,
        blank=True
    )

    clinic_visit = models.CharField(
        verbose_name="Have you been seen at a local clinic or have you been seen for "
                     "consultation at a local clinic because of this illness?",
        max_length=20,
        choices=CLINIC_VISIT_CHOICES,
        blank=True,
        null=True
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Medical History'
        verbose_name_plural = 'Medical History'
