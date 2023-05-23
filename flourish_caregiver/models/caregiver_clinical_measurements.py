from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_constants.choices import YES_NO

from .model_mixins import CrfModelMixin


class CaregiverClinicalMeasurements(CrfModelMixin):
    """ A model completed by the user on Height, Weight details
    for all cregivers. """

    # field changed to be saved as null because the field
    # is not required at birth visit
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Caregiver\'s height? ',
        validators=[MinValueValidator(130), MaxValueValidator(210), ],
        null=True,
        blank=True,
        help_text='Measured in Centimeters (cm)')

    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Caregiver\'s weight? ',
        validators=[MinValueValidator(40), MaxValueValidator(140), ],
        help_text='Measured in Kilograms (kg)')

    systolic_bp = models.IntegerField(
        verbose_name='Caregiver\'s systolic blood pressure?',
        help_text='in mm e.g. 120, normal values are between 100 and 130.',
        null=True,
        blank=True,
    )

    diastolic_bp = models.IntegerField(
        verbose_name='Caregiver\'s diastolic blood pressure?',
        help_text='in hg e.g. 80, normal values are between 60 and 80.',
        null=True,
        blank=True,
    )

    confirm_values = models.CharField(
        verbose_name='Are you sure about given values',
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True,
    )

    waist_circ = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Caregiver\'s waist circumference first measurement',
        validators=[MinValueValidator(50), MaxValueValidator(420), ],
        null=True,
        blank=True,
        help_text=('only measure waist circumference for caregivers who are '
                   'not pregnant'))

    hip_circ = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Caregiver\'s hip circumference first measurement',
        validators=[MinValueValidator(50), MaxValueValidator(420), ],
        null=True,
        blank=True,
        help_text=('Only measure waist circumference for caregivers who are '
                   'not pregnant'))

    all_measurements = models.CharField(
        verbose_name='Were you able to obtain all clinical measurement at this visit',
        max_length=3,
        choices=YES_NO,

    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Clinical Measurements'
        verbose_name_plural = 'Caregiver Clinical Measurements'
