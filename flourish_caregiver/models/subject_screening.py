from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from ..identifiers import ScreeningIdentifier
from .eligibility import Eligibility
from .model_mixins import SearchSlugModelMixin


class SubjectScreeningManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, eligibility_identifier):
        return self.get(screening_identifier=eligibility_identifier)


class SubjectScreening(NonUniqueSubjectIdentifierFieldMixin, SiteModelMixin,
                       SearchSlugModelMixin, BaseUuidModel):
    """ A model completed by the user to test and capture the result of
    the pre-consent eligibility checks.

    This model has no PII.
    """
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

    age_in_years = models.IntegerField(
        verbose_name='What is the age of the participant?')

    has_omang = models.CharField(
        verbose_name="Do you have an OMANG?",
        max_length=3,
        choices=YES_NO)

    has_child = models.CharField(
        verbose_name="Do you have a child who is 10 years or older?",
        max_length=3,
        choices=YES_NO)

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
    # updated by signal on saving consent, is determined by participant
    # citizenship
    has_passed_consent = models.BooleanField(
        default=False,
        editable=False)

    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Maternal Eligibility"
        verbose_name_plural = "Maternal Eligibility"

    def save(self, *args, **kwargs):
        eligibility_criteria = Eligibility(self.age_in_years, self.has_omang)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        if not self.screening_identifier:
            self.screening_identifier = self.identifier_cls().identifier
        super(SubjectScreening, self).save(*args, **kwargs)

    def natural_key(self):
        return self.screening_identifier

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('screening_identifier')
        return fields
