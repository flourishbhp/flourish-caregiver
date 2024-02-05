from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_fields import OtherCharField

from .model_mixins import CrfModelMixin
from ..choices import (PERIOD_HAPPENED, HAPPENED,
                       PERIOD_HAPPENED_DONT_KNOW, HAPPENED_DONT_KNOW, HIV_PERSPECTIVE)


class CaregiverSafiStigma(CrfModelMixin):
    """ A model completed by the user on Height, Weight details
    for all caregivers. """

    judged_negatively = models.CharField(
        verbose_name='Because someone else in my family has HIV or '
        'because I have HIV, I am judged negatively by others ',
        max_length=20,
        choices=HAPPENED
    )

    judged_negatively_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    isolated = models.CharField(
        verbose_name='Because someone else in my family has HIV or because I have HIV, I am isolated or avoided by others',
        choices=HAPPENED,
        max_length=20
    )

    isolated_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    insulted = models.CharField(
        verbose_name='Because someone else in my family has HIV or because I have HIV, I have been called names or insulted',
        max_length=20,
        choices=HAPPENED
    )

    insualted_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    discriminated_at_home = models.CharField(
        verbose_name='Home',
        max_length=20,
        choices=HAPPENED
    )

    discriminated_at_home_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    discriminated_at_neigborhood = models.CharField(
        verbose_name='Neigborhood',
        max_length=20,
        choices=HAPPENED
    )

    discriminated_at_neigborhood_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    discriminated_at_religious = models.CharField(
        verbose_name='A Religious Place (e.g. church)',
        max_length=20,
        choices=HAPPENED
    )

    discriminated_at_religious_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    discriminated_at_clinic = models.CharField(
        verbose_name='Clinic',
        max_length=20,
        choices=HAPPENED
    )

    discriminated_at_clinic_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    discriminated_at_workplace = models.CharField(
        verbose_name='Workplace',
        max_length=20,
        choices=HAPPENED
    )

    discriminated_at_workplace_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    lose_finacial_support = models.CharField(
        verbose_name='Lose Financial Support/Work',
        max_length=20,
        choices=HAPPENED
    )

    lose_finacial_support_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    lose_social_support = models.CharField(
        verbose_name='Lose Social Support',
        max_length=20,
        choices=HAPPENED
    )

    lose_social_support_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    stressed_or_anxious = models.CharField(
        verbose_name='Lose Social Support',
        max_length=20,
        choices=HAPPENED,

    )

    stressed_or_anxious_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    depressed_or_saddened = models.CharField(
        verbose_name='Depressed, feeling down, saddened ',
        max_length=20,
        choices=HAPPENED,
    )

    depressed_or_saddened_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    community_hiv_perspective = models.CharField(
        verbose_name='People in the community think that HIV is a “dirty,” “immoral,” or “shameful” disease ',
        choices=HIV_PERSPECTIVE,
        max_length=25
    )

    caregiver_isolated = models.CharField(
        verbose_name='Because of my HIV status, I am isolated or avoided by other children or adults',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    caregiver_isolated_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    caregiver_insulted = models.CharField(
        verbose_name='Because of my HIV status, I have been called names, insulted, or bullied ',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    caregiver_insulted_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    caregiver_home_discrimination = models.CharField(
        verbose_name='Home',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    caregiver_home_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    caregiver_neighborhood_discrimination = models.CharField(
        verbose_name='Neighborhood',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    caregiver_neighborhood_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    caregiver_religious_place_discrimination = models.CharField(
        verbose_name=' A Religious Place (e.g. church)',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    caregiver_religious_place_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    caregiver_clinic_discrimination = models.CharField(
        verbose_name=' A Religious Place (e.g. church)',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    caregiver_clinic_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    caregiver_school_discrimination = models.CharField(
        verbose_name=' A Religious Place (e.g. church)',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    caregiver_school_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    caregiver_other_discrimination = models.CharField(
        verbose_name='Other Place',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    caregiver_other_discrimination_other = OtherCharField()

    caregiver_other_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW
    )

    caregiver_social_effect = models.CharField(
        verbose_name='Socially',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
        null=True,
    )

    caregiver_social_effect_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,

    )

    caregiver_emotional_effect = models.CharField(
        verbose_name='Socially',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
        null=True,
    )

    caregiver_emotional_effect_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    caregiver_education_effect = models.CharField(
        verbose_name='In his/her Education ',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
        null=True,

    )

    caregiver_education_effect_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    caregiver_future_pespective_changed = models.CharField(
        verbose_name='Because of the child’s HIV status, how the future is viewed by him/her '
        'or future hopes that this child has for himself/herself have changed in a negative way',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,

    )

    caregiver_future_pespective_changed_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver SAFI Stigma'
        verbose_name_plural = 'Caregiver SAFI Stigma'
