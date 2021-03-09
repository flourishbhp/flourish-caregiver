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
from edc_constants.choices import YES_NO

from ..choices import IDENTITY_TYPE, COHORTS
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

    child_test = models.CharField(
        verbose_name='Will you allow for HIV testing and counselling of '
                     'your Child',
        max_length=5,
        choices=YES_NO)

    child_remain_in_study = models.CharField(
        verbose_name='Is your child willing to remain in the study area until 2025?',
        max_length=5,
        choices=YES_NO)

    child_preg_test = models.CharField(
        verbose_name='If your child is female and will be 12 years or older '
                     'prior to 30-Jun-2025, will you allow the female child '
                     'to undergo pregnancy testing?',
        max_length=5,
        choices=YES_NO,
        blank=True,
        null=True,)

    child_knows_status = models.CharField(
        verbose_name='If your child is ≥ 16 years, have they been told about your HIV?',
        max_length=5,
        choices=YES_NO,
        blank=True,
        null=True)

    cohort = models.CharField(
        max_length=12,
        choices=COHORTS,
        blank=True,
        null=True)

    child_dob = models.DateField(
        verbose_name="Date of birth",
        null=True,
        blank=False)

    child_age_at_enrollment = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=4)

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
            self.consent_signature, self.consent_copy)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        self.version = '1'
        self.child_age_at_enrollment = self.get_child_age_at_enrollment()
        if self.is_eligible:
            if self.id and not self.subject_identifier:
                self.subject_identifier = self.update_subject_identifier_on_save()
        super().save(*args, **kwargs)

    def get_child_age_at_enrollment(self):
        from ..helper_classes import Cohort
        from .maternal_dataset import MaternalDataset

        try:
            maternal_dataset = MaternalDataset.objects.get(
                screening_identifier=self.screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            self.child_dob = maternal_dataset.delivdt
            return Cohort(
                ).age_at_enrollment(
                    child_dob=self.child_dob,
                    check_date=self.created.date())

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
            if not getattr(self, self.registration_unique_field):
                raise UpdatesOrCreatesRegistrationModelError(
                    f'Cannot update or create RegisteredSubject. '
                    f'Field value for \'{self.registration_unique_field}\' is None.')

            registration_value = getattr(self, self.registration_unique_field)
            registration_value = self.to_string(registration_value)

            try:
                obj = self.registration_model.objects.get(
                    **{self.registered_subject_unique_field: registration_value})
            except self.registration_model.DoesNotExist:
                pass
            else:
                self.registration_raise_on_illegal_value_change(obj)
            registered_subject, created = self.registration_model.objects.update_or_create(
                **{self.registered_subject_unique_field: registration_value},
                defaults=self.registration_options)
            return registered_subject, created

    class Meta(ConsentModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Adult Participation Consent'
        unique_together = (('subject_identifier', 'version'),
                           ('subject_identifier', 'screening_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
