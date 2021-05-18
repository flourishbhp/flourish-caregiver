from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from ..maternal_choices import KNOW_HIV_STATUS
from .list_models import ChronicConditions, CaregiverMedications, WcsDxAdult
from .model_mixins import CrfModelMixin


class MedicalHistory(CrfModelMixin):

    """A model completed by the user on Medical History for all care givers."""

    chronic_since = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name='Does the caregiver have any chronic conditions?',)

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
        max_length=20,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Medical History'
        verbose_name_plural = 'Medical History'
