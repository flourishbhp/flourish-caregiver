from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO

from flourish_caregiver.choices import YES_NO_UNK_NO_CHILD
from flourish_caregiver.models.model_mixins import CrfModelMixin
from flourish_child.choices import (BUILT_DATES, BUSINESSES_RUN,
                                    CAREGIVER_EDUCATION_LEVEL_CHOICES)


class ChildhoodLeadExposureRisk(CrfModelMixin):
    residence_age = models.DecimalField(
        verbose_name='How long have you lived at your current residence? ',
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        decimal_places=1,
        max_digits=4,
        help_text='years'
    )

    lead_exposure_test = models.CharField(
        verbose_name='Has your child ever been tested for lead exposure?',
        max_length=7,
        choices=YES_NO,
    )

    suck_fingers = models.CharField(
        verbose_name='Does your child suck any of his/her fingers?',
        max_length=7,
        choices=YES_NO,
    )

    eats_soil = models.CharField(
        verbose_name='Have you ever observed your child eating soil?',
        max_length=7,
        choices=YES_NO,
    )

    eats_paint_chips = models.CharField(
        verbose_name='Have you ever observed your child eating paint chips? ',
        max_length=7,
        choices=YES_NO,
    )

    eating_keys = models.CharField(
        verbose_name='Have you ever observed your child putting keys in his/her mouth?',
        max_length=7,
        choices=YES_NO,
    )

    eating_jewellery = models.CharField(
        verbose_name='Have you ever observed your child putting jewellery in his /her '
                     'mouth? ',
        max_length=7,
        choices=YES_NO,
    )

    relative_paints = models.CharField(
        verbose_name='Does your child live with a relative who paints houses?',
        max_length=7,
        choices=YES_NO
    )

    home_business = models.CharField(
        verbose_name='Does anyone in your home run a personal or family business?',
        max_length=7,
        choices=YES_NO,
    )

    home_run_business = models.CharField(
        verbose_name='What business is run from the home?',
        blank=True,
        choices=BUSINESSES_RUN,
        null=True,
        max_length=50,
    )

    home_run_business_other = models.TextField(
        verbose_name='if Other, specify',
        blank=True,
        null=True
    )

    relative_work_batteries = models.CharField(
        verbose_name='Does your child live with a relative who works in a place '
                     'where car batteries are made?',
        max_length=7,
        choices=YES_NO,
    )

    relative_repairs_cars = models.CharField(
        verbose_name='Does your child live with a relative who repairs cars?',
        max_length=7,
        choices=YES_NO,
    )

    unusable_vehicles = models.CharField(
        verbose_name='Do you have any unusable vehicles in your yard?',
        max_length=7,
        choices=YES_NO,
    )

    traditional_remedies = models.CharField(
        verbose_name='Does your child consume any traditional plant-based/herbal '
                     'remedies?',
        max_length=7,
        choices=YES_NO,
    )

    peeling_paint = models.CharField(
        verbose_name='Is there any peeling, chipping or cracking paint in your home?',
        max_length=30,
        choices=YES_NO_UNK_NO_CHILD,
    )

    house_by_busy_road = models.CharField(
        verbose_name='Since your child was born, have you ever lived in a home next to a '
                     'busy road',
        max_length=30,
        choices=YES_NO_UNK_NO_CHILD,
    )

    years_near_busy_road = models.DecimalField(
        verbose_name='How many years did your child live in a home next to a busy road',
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        decimal_places=1,
        max_digits=4,
    )

    pr_male_caregiver_edu = models.CharField(
        verbose_name='Education level of primary male caregiver',
        max_length=45,
        choices=CAREGIVER_EDUCATION_LEVEL_CHOICES
    )

    child_restless = models.CharField(
        verbose_name='Would you consider this child to be restless?',
        max_length=7,
        choices=YES_NO,
    )

    house_year_built = models.CharField(
        verbose_name='When was the house you live in now built?',
        max_length=15,
        choices=BUILT_DATES
    )

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Childhood Lead Exposure Risk'
        verbose_name_plural = 'Childhood Lead Exposure Risks'
