from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_fields import OtherCharField

from .model_mixins import CrfModelMixin
from ..choices import (PERIOD_HAPPENED, HAPPENED,
                       PERIOD_HAPPENED_DONT_KNOW, HAPPENED_DONT_KNOW,
                       HAPPENED_DONT_KNOW_WITH_NA, HIV_PERSPECTIVE)


class CaregiverSafiStigma(CrfModelMixin):
    """ A model completed by the user on Height, Weight details
    for all caregivers. """

    judged = models.CharField(
        verbose_name='Because someone else in my family has HIV or '
        'because I have HIV, I am judged negatively by others ',
        max_length=20,
        choices=HAPPENED
    )

    judged_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    avoided = models.CharField(
        verbose_name='Because someone else in my family has HIV or because I have HIV, I am isolated or avoided by others',
        choices=HAPPENED,
        max_length=20
    )

    avoided_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    discriminated = models.CharField(
        verbose_name='Because someone else in my family has HIV or because I have HIV, I have been called names or insulted',
        max_length=20,
        choices=HAPPENED
    )

    discriminated_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    at_home = models.CharField(
        verbose_name='Home',
        max_length=20,
        choices=HAPPENED
    )

    at_home_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    at_neigborhood = models.CharField(
        verbose_name='Neigborhood',
        max_length=20,
        choices=HAPPENED
    )

    at_neigborhood_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    at_religious = models.CharField(
        verbose_name='A Religious Place (e.g. church)',
        max_length=20,
        choices=HAPPENED
    )

    at_religious_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    at_clinic = models.CharField(
        verbose_name='Clinic',
        max_length=20,
        choices=HAPPENED
    )

    at_clinic_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    at_workplace = models.CharField(
        verbose_name='Workplace',
        max_length=20,
        choices=HAPPENED
    )

    at_workplace_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    finacial_support = models.CharField(
        verbose_name='Lose Financial Support/Work',
        max_length=20,
        choices=HAPPENED
    )

    finacial_support_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    social_support = models.CharField(
        verbose_name='Lose Social Support',
        max_length=20,
        choices=HAPPENED
    )

    social_support_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    stressed = models.CharField(
        verbose_name='Lose Social Support',
        max_length=20,
        choices=HAPPENED,

    )

    stressed_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    saddened = models.CharField(
        verbose_name='Depressed, feeling down, saddened ',
        max_length=20,
        choices=HAPPENED,
    )

    saddened_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    hiv_perspective = models.CharField(
        verbose_name='People in the community think that HIV is a “dirty,” “immoral,” or “shameful” disease ',
        choices=HIV_PERSPECTIVE,
        max_length=25,
        null=True,

    )

    isolated = models.CharField(
        verbose_name='Because of my HIV status, I am isolated or avoided by other children or adults',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
        null=True,
    )

    isolated_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    insulted = models.CharField(
        verbose_name='Because of my HIV status, I have been called names, insulted, or bullied ',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
        null=True,

    )

    insulted_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    home_discr = models.CharField(
        verbose_name='Home',
        max_length=20,
        choices=HAPPENED_DONT_KNOW_WITH_NA,
        null=True,

    )

    home_discr_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    neighborhood_discr = models.CharField(
        verbose_name='Neighborhood',
        max_length=20,
        choices=HAPPENED_DONT_KNOW_WITH_NA,
        null=True,

    )

    neighborhood_discr_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    religious_place_discr = models.CharField(
        verbose_name=' A Religious Place (e.g. church)',
        max_length=20,
        choices=HAPPENED_DONT_KNOW_WITH_NA,
        null=True,

    )

    religious_place_discr_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    clinic_discr = models.CharField(
        verbose_name=' A Religious Place (e.g. church)',
        max_length=20,
        choices=HAPPENED_DONT_KNOW_WITH_NA,
        null=True,

    )

    clinic_discr_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    school_discr = models.CharField(
        verbose_name=' A Religious Place (e.g. church)',
        max_length=20,
        choices=HAPPENED_DONT_KNOW_WITH_NA,
        null=True,

    )

    school_discr_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    other_discr = models.CharField(
        verbose_name='Other Place',
        max_length=20,
        choices=HAPPENED_DONT_KNOW_WITH_NA,
        blank=True,
        null=True,
    )

    other_discr_other = OtherCharField()

    other_discr_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        null=True,

    )

    social_effect = models.CharField(
        verbose_name='Socially',
        max_length=20,
        choices=HAPPENED_DONT_KNOW_WITH_NA,
        null=True,
    )

    social_effect_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,

    )

    emotional_effect = models.CharField(
        verbose_name='Emotionally (for example, you feel stressed, down, or depressed)',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
        null=True,
    )

    emotional_effect_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    pespective_changed = models.CharField(
        verbose_name=(' Because of my HIV status, how the future is viewed by myself'
                      ' or future hopes that I have has changed in a negative way'),
        max_length=20,
        choices=HAPPENED_DONT_KNOW_WITH_NA,

    )

    pespective_changed_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver SAFI Stigma'
        verbose_name_plural = 'Caregiver SAFI Stigma'
