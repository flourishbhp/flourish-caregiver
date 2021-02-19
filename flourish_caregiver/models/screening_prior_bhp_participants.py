from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from .eligibility import BHPPriorEligibilty
from ..choices import FLOURISH_PARTICIPATION, YES_NO_UNK_NA


class ScreeningPriorBhpParticipants(SiteModelMixin, BaseUuidModel):

    screening_identifier = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        blank=True,
        null=True,
        unique=True)

    study_child_identifier = models.CharField(
        verbose_name='Study Child Subject Identifier',
        max_length=50,
        unique=True)

    child_alive = models.CharField(
        verbose_name='Is the child from the previous study alive?',
        max_length=10,
        choices=YES_NO)

    mother_alive = models.CharField(
        verbose_name='Is the mother from the previous study alive?',
        max_length=10,
        choices=YES_NO_UNK_NA,
        default=NOT_APPLICABLE)

    flourish_interest = models.CharField(
        verbose_name='Is there another caregiver within the household '
                     'that would be interested in learning about FLOURISH '
                     'study?',
        max_length=10,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    flourish_participation = models.CharField(
        verbose_name='Are you or another caregiver of this child interested in'
                     ' participating in the FLOURISH Study ',
        max_length=40,
        choices=FLOURISH_PARTICIPATION,
        default=NOT_APPLICABLE)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    def save(self, *args, **kwargs):
        eligibility_criteria = BHPPriorEligibilty(
            self.child_alive, self.flourish_interest, self.flourish_participation)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Screening Prior BHP Participants'
        verbose_name_plural = 'Screening Prior BHP Participants'


