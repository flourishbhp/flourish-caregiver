from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_registration.model_mixins.updates_or_creates_registered_subject_model_mixin import (
    UpdatesOrCreatesRegistrationModelError)
from edc_registration.model_mixins import (
    UpdatesOrCreatesRegistrationModelMixin)
from edc_search.model_mixins import SearchSlugManager

from edc_consent.field_mixins import (
    CitizenFieldsMixin, VulnerabilityFieldsMixin)
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_consent.field_mixins import PersonalFieldsMixin
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO, GENDER

from ..choices import IDENTITY_TYPE
from ..maternal_choices import RECRUIT_SOURCE, RECRUIT_CLINIC
from ..subject_identifier import SubjectIdentifier
from .eligibility import ConsentEligibility
from .model_mixins import ReviewFieldsMixin, SearchSlugModelMixin


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

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        null=True)

    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
        max_length=50)

    gender = models.CharField(
        verbose_name='Gender',
        choices=GENDER,
        max_length=1,)

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
        verbose_name="if other recruitment, specify...",
        blank=True,
        null=True,)

    remain_in_study = models.CharField(
        max_length=3,
        verbose_name='Are you willing to remain in the study area until 2025?',
        choices=YES_NO,
        help_text='If no, participant is not eligible.')

    hiv_testing = models.CharField(
        max_length=3,
        verbose_name=('If HIV status not known, are you willing to undergo HIV'
                      ' testing and counseling?'),
        choices=YES_NO,
        blank=True,
        null=True,
        help_text='If ‘No’ ineligible for study participation')

    breastfeed_intent = models.CharField(
        max_length=3,
        verbose_name='Do you intend on breast feeding your infant?',
        choices=YES_NO,
        blank=True,
        null=True,
        help_text='If ‘No’ ineligible for study participation')

    future_contact = models.CharField(
        max_length=3,
        verbose_name='Do you give us permission to be contacted for future studies?',
        choices=YES_NO)

    child_consent = models.CharField(
        max_length=3,
        verbose_name='Are you willing to consent for your child’s participation in FLOURISH?',
        choices=YES_NO,
        help_text='If ‘No’ ineligible for study participation')

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    objects = SubjectConsentManager()

    consent = ConsentManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.subject_identifier} V{self.version}'

    def save(self, *args, **kwargs):
        eligibility_criteria = ConsentEligibility(
            self.remain_in_study, self.hiv_testing, self.breastfeed_intent,
            self.consent_reviewed, self.study_questions, self.assessment_score,
            self.consent_signature, self.consent_copy, self.child_consent)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        self.version = '1'
        if self.is_eligible:
            if self.created and not self.subject_identifier:
                self.subject_identifier = self.update_subject_identifier_on_save()
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.subject_identifier, self.version)

    def make_new_identifier(self):
        """Returns a new and unique identifier.

        Override this if needed.
        """
        if not self.is_eligible:
            return None
        subject_identifier = SubjectIdentifier(
            identifier_type='subject',
            requesting_model=self._meta.label_lower,
            site=self.site)
        return subject_identifier.identifier

    @property
    def consent_version(self):
        return self.version

    def registration_update_or_create(self):
        """Creates or Updates the registration model with attributes
        from this instance.

        Called from the signal
        """
        if self.is_eligible:
            return super().registration_update_or_create()

    class Meta(ConsentModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Adult Participation Consent'
        unique_together = (('subject_identifier', 'version'),
                           ('screening_identifier', 'version'),
                           ('subject_identifier', 'screening_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
