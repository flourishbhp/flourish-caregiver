from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_registration.model_mixins import (
    UpdatesOrCreatesRegistrationModelMixin)
from edc_search.model_mixins import SearchSlugManager

from edc_consent.field_mixins import (
    CitizenFieldsMixin, VulnerabilityFieldsMixin)
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_consent.field_mixins import ReviewFieldsMixin, PersonalFieldsMixin
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_consent.validators import eligible_if_yes
from edc_constants.choices import YES_NO

from ..choices import IDENTITY_TYPE
from ..maternal_choices import RECRUIT_SOURCE, RECRUIT_CLINIC
from ..subject_identifier import SubjectIdentifier
from .model_mixins import SearchSlugModelMixin


class SubjectConsentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier, version):
        return self.get(
            subject_identifier=subject_identifier, version=version)


class SubjectConsent(
        ConsentModelMixin, SiteModelMixin,
        UpdatesOrCreatesRegistrationModelMixin,
        NonUniqueSubjectIdentifierModelMixin, IdentityFieldsMixin,
        ReviewFieldsMixin, PersonalFieldsMixin, CitizenFieldsMixin,
        VulnerabilityFieldsMixin, SearchSlugModelMixin, BaseUuidModel):

    """ A model completed by the user on the mother's consent. """

    subject_screening_model = 'flourish_caregiver.subjectscreening'

    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
        max_length=50)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=IDENTITY_TYPE)

    recruit_source = models.CharField(
        max_length=75,
        choices=RECRUIT_SOURCE,
        verbose_name="The caregiver first learned about the flourish "
        "study from ")

    recruit_source_other = OtherCharField(
        max_length=35,
        verbose_name="if other recruitment source, specify...",
        blank=True,
        null=True)

    recruitment_clinic = models.CharField(
        max_length=100,
        verbose_name="The caregiver was recruited from",
        choices=RECRUIT_CLINIC)

    recruitment_clinic_other = models.CharField(
        max_length=100,
        verbose_name="if other recruitment clinic, specify...",
        blank=True,
        null=True,)

    remain_in_study = models.CharField(
        max_length=3,
        verbose_name='Are you willing to remain in the study area for 5 years?',
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text='If no, participant is not eligible.')

    hiv_testing = models.CharField(
        max_length=3,
        verbose_name=('If HIV status not known, are you willing to undergo HIV'
                      ' testing and counseling?'),
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text='If ‘No’ ineligible for study participation')

    breastfeed_intent = models.CharField(
        max_length=3,
        verbose_name='Do you intend on breast feeding your infant?',
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text='If ‘No’ ineligible for study participation')

    future_contact = models.CharField(
        max_length=3,
        verbose_name='Do you give us permission to be contacted for future studies?',
        choices=YES_NO)

    objects = SubjectConsentManager()

    consent = ConsentManager()

    history = HistoricalRecords()

    _cohort_schedule = None

    def __str__(self):
        return f'{self.subject_identifier} V{self.version}'

    def natural_key(self):
        return (self.subject_identifier, self.version)

    def make_new_identifier(self):
        """Returns a new and unique identifier.

        Override this if needed.
        """
        subject_identifier = SubjectIdentifier(
            identifier_type='subject',
            requesting_model=self._meta.label_lower,
            site=self.site)
        return subject_identifier.identifier

    @property
    def cohort(self):
        #TO-DO: add variable name, e.g 'cohort_a'
        return self._cohort_schedule

    @cohort.setter
    def cohort(self, val):
        self._cohort_schedule = val

    @property
    def consent_version(self):
        return self.version

    class Meta(ConsentModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Adult Participation Consent'
        unique_together = (('subject_identifier', 'version'),
                           ('subject_identifier', 'screening_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
