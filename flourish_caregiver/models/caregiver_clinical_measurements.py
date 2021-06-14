from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .model_mixins import CrfModelMixin


class CaregiverClinicalMeasurements(CrfModelMixin):
    """ A model completed by the user on Height, Weight details
    for all cregivers. """

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Caregiver\'s height? ',
        validators=[MinValueValidator(114), MaxValueValidator(195), ],
        help_text='Measured in Centimeters (cm)')

    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Caregiver\'s weight? ',
        validators=[MinValueValidator(30), MaxValueValidator(160), ],
        help_text='Measured in Kilograms (kg)')

    systolic_bp = models.IntegerField(
        verbose_name='Caregiver\'s systolic blood pressure?',
        validators=[MinValueValidator(75), MaxValueValidator(220), ],
        help_text='in mm e.g. 120, should be between 75 and 220.'
    )

    diastolic_bp = models.IntegerField(
        verbose_name='Caregiver\'s diastolic blood pressure?',
        validators=[MinValueValidator(35), MaxValueValidator(150), ],
        help_text='in hg e.g. 80, should be between 35 and 150.')

    waist_circ = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Caregiver\'s waist circumference',
        validators=[MinValueValidator(50), MaxValueValidator(420), ],
        help_text=('only measure waist circumference for caregivers who are '
                   'not pregnant'))

    hip_circ = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Caregiver\'s hip circumference',
        validators=[MinValueValidator(50), MaxValueValidator(420), ],
        help_text=('only measure waist circumference for caregivers who are '
                   'not pregnant'))

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Clinical Measurements'
        verbose_name_plural = 'Caregiver Clinical Measurements'
