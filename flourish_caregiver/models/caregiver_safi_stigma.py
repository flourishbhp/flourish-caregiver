from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE

from .model_mixins import CrfModelMixin
from ..choices import (PERIOD_HAPPENED, HAPPENED,
                       PERIOD_HAPPENED_DONT_KNOW, HAPPENED_DONT_KNOW,
                       HIV_PERSPECTIVE)


class CaregiverSafiStigma(CrfModelMixin):
    """ The model is based off form for caregivers not living with HIV. Some
        questions are updated on the admin for caregivers LWHIV."""

    member_lwhiv = models.CharField(
        verbose_name=('Do you have a family member or someone who you are '
                      'close with who is living with HIV?'),
        max_length=3,
        choices=YES_NO)

    judged = models.CharField(
        verbose_name=('Because someone else in my family or a close friend '
                      'has HIV, I am judged negatively by others'),
        max_length=20,
        choices=HAPPENED,
        default=NOT_APPLICABLE
    )

    judged_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    avoided = models.CharField(
        verbose_name=('Because someone else in my family or a close friend '
                      'has HIV, I am isolated or avoided by others'),
        choices=HAPPENED,
        max_length=20,
        default=NOT_APPLICABLE
    )

    avoided_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    discriminated = models.CharField(
        verbose_name=('Because someone else in my family or a close friend '
                      'has HIV, I have been called names or insulted'),
        max_length=20,
        choices=HAPPENED,
        default=NOT_APPLICABLE
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
        choices=HAPPENED,
        default=NOT_APPLICABLE
    )

    at_home_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    at_neigborhood = models.CharField(
        verbose_name='Neighborhood',
        max_length=20,
        choices=HAPPENED,
        default=NOT_APPLICABLE
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
        choices=HAPPENED,
        default=NOT_APPLICABLE
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
        choices=HAPPENED,
        default=NOT_APPLICABLE
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
        choices=HAPPENED,
        default=NOT_APPLICABLE
    )

    at_workplace_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    other_place = models.CharField(
        verbose_name='Other place, (please specify)',
        max_length=100,
        null=True,
        blank=True)

    other_place_period = models.CharField(
        verbose_name='If “Ever Happened” at Other Place: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        null=True,
        blank=True
    )

    finacial_support = models.CharField(
        verbose_name='Lose Financial Support/Work',
        max_length=20,
        choices=HAPPENED,
        default=NOT_APPLICABLE
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
        choices=HAPPENED,
        default=NOT_APPLICABLE
    )

    social_support_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    stressed = models.CharField(
        verbose_name='Stressed or anxious',
        max_length=20,
        choices=HAPPENED,
        default=NOT_APPLICABLE
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
        default=NOT_APPLICABLE
    )

    saddened_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    hiv_perspective = models.CharField(
        verbose_name=('People in the community think that HIV is a “dirty,”'
                      ' “immoral,” or “shameful” disease '),
        choices=HIV_PERSPECTIVE,
        max_length=25,
        null=True,

    )

    """ The following section is questions ONLY to be shown for participants
        living with HIV.
    """

    social_effect = models.CharField(
        verbose_name='Socially',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
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
        verbose_name=('Because of my HIV status, how the future is viewed by myself'
                      ' or future hopes that I have has changed in a negative way'),
        max_length=20,
        choices=HAPPENED_DONT_KNOW,

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
