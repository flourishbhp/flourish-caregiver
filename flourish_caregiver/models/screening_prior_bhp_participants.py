from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from .eligibility import BHPPriorEligibilty
from .model_mixins import SearchSlugModelMixin
from ..choices import FLOURISH_PARTICIPATION, YES_NO_UNK_NA, REASONS_NOT_PARTICIPATE
from ..identifiers import ScreeningIdentifier


class ScreeningPriorBhpParticipantsManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, eligibility_identifier):
        return self.get(screening_identifier=eligibility_identifier)


class ScreeningPriorBhpParticipants(NonUniqueSubjectIdentifierFieldMixin, SiteModelMixin,
                                    SearchSlugModelMixin, BaseUuidModel):
    identifier_cls = ScreeningIdentifier

    screening_identifier = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        blank=True,
        null=True,
        unique=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=get_utcnow,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        help_text='Date and time of assessing eligibility')

    study_maternal_identifier = models.CharField(
        verbose_name="Study Caregiver Subject Identifier",
        max_length=50,
        blank=True,
        null=True)

    child_alive = models.CharField(
        verbose_name='Is the child from the previous study alive?',
        max_length=10,
        choices=YES_NO)

    mother_alive = models.CharField(
        verbose_name='Is the biological mother from the previous study alive?',
        max_length=10,
        choices=YES_NO_UNK_NA,
        default=NOT_APPLICABLE)

    flourish_participation = models.CharField(
        verbose_name='Are you or another caregiver of this child interested in'
                     ' participating in the FLOURISH Study? ',
        max_length=40,
        choices=FLOURISH_PARTICIPATION,
        default=NOT_APPLICABLE)

    reason_not_to_participate = models.CharField(
        verbose_name='What is the reason the participant is unwilling to participate in '
                     'the study:',
        max_length=80,
        choices=REASONS_NOT_PARTICIPATE,
        default=NOT_APPLICABLE
    )

    reason_not_to_participate_other = OtherCharField(
        verbose_name='If other, specify')

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    # is updated via signal once subject is consented
    is_consented = models.BooleanField(
        default=False,
        editable=False)

    history = HistoricalRecords()

    objects = ScreeningPriorBhpParticipantsManager()

    def __str__(self):
        return f'{self.screening_identifier}, {self.study_maternal_identifier}'

    def save(self, *args, **kwargs):
        eligibility_criteria = BHPPriorEligibilty(
            self.child_alive, self.mother_alive, self.flourish_participation,
            )
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        if not self.screening_identifier:
            self.screening_identifier = self.identifier_cls().identifier
        super().save(*args, **kwargs)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('screening_identifier')
        fields.append('study_maternal_identifier')
        return fields

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Screening Prior BHP Participants'
        verbose_name_plural = 'Screening Prior BHP Participants'
