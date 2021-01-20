from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_constants.choices import YES_NO_UNKNOWN, YES_NO

from ..choices import FLOURISH_PARTICIPATION


class ScreeningPriorBhpParticipants(SiteModelMixin, BaseUuidModel):

    study_child_identifier = models.CharField(
        verbose_name='Study Child Subject Identifier',
        max_length=50,
        unique=True)

    child_alive = models.CharField(
        verbose_name='Is the child from the previous study alive?',
        max_length=10,
        choices=YES_NO_UNKNOWN,
        blank=False,
        null=False)

    mother_alive = models.CharField(
        verbose_name='Is the mother from the previous study alive?',
        max_length=10,
        choices=YES_NO_UNKNOWN,
        blank=False,
        null=False)

    flourish_interest = models.CharField(
        verbose_name='Is there another caregiver within the household '
                     'that would be interested in learning about FLOURISH '
                     'study?',
        max_length=10,
        choices=YES_NO,
        blank=True,
        null=True)

    age_assurance = models.CharField(
        verbose_name='Does the caregiver provide assurance they are 18 years '
                     'of age or older?',
        max_length=7,
        choices=YES_NO,
        blank=True,
        null=True)

    flourish_participation = models.CharField(
        verbose_name='Are you or another caregiver of this child interested in'
                     ' participating in the FLOURISH Study ',
        max_length=40,
        choices=FLOURISH_PARTICIPATION,
        blank=False,
        null=False)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Screening Prior BHP Participants'
        verbose_name_plural = 'Screening Prior BHP Participants'


