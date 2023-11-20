from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.field_mixins import (
    CitizenFieldsMixin, VulnerabilityFieldsMixin)
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_consent.field_mixins import PersonalFieldsMixin
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO, GENDER, YES_NO_NA
from edc_constants.constants import NO, YES, FEMALE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_search.model_mixins import SearchSlugManager

from ..choices import IDENTITY_TYPE
from ..maternal_choices import RECRUIT_SOURCE, RECRUIT_CLINIC
from ..subject_identifier import SubjectIdentifier
from .eligibility import ConsentEligibility
from .model_mixins import ReviewFieldsMixin, SearchSlugModelMixin


class SubjectConsentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier, version):
        return self.get(
            subject_identifier=subject_identifier, version=version)


class SubjectConsent(ConsentModelMixin, SiteModelMixin,
                     UpdatesOrCreatesRegistrationModelMixin,
                     NonUniqueSubjectIdentifierModelMixin, IdentityFieldsMixin,
                     ReviewFieldsMixin, PersonalFieldsMixin, CitizenFieldsMixin,
                     VulnerabilityFieldsMixin, SearchSlugModelMixin, BaseUuidModel):
    """ A model completed by the user on the mother's consent. """

    subject_screening_model = 'flourish_caregiver.subjectscreening'

    caregiver_locator_model = 'flourish_caregiver.caregiverlocator'

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
        max_length=1,
        default=FEMALE)

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

    biological_caregiver = models.CharField(
        max_length=3,
        verbose_name='Are you the biological mother to the child or children?',
        choices=YES_NO,
        blank=True)

    hiv_testing = models.CharField(
        max_length=3,
        verbose_name=('If HIV status not known, are you willing to undergo HIV'
                      ' testing and counseling?'),
        choices=YES_NO_NA,
        help_text='If ‘No’ ineligible for study participation')

    breastfeed_intent = models.CharField(
        max_length=3,
        verbose_name='Do you intend on breast feeding your infant?',
        choices=YES_NO_NA,
        help_text='If ‘No’ ineligible for study participation')

    future_contact = models.CharField(
        max_length=3,
        verbose_name='Do you give us permission to be contacted for future studies?',
        choices=YES_NO)

    child_consent = models.CharField(
        max_length=3,
        verbose_name='Are you willing to consent for your child’s participation in FLOURISH?',
        choices=YES_NO_NA,
        help_text='If ‘No’ ineligible for study participation')

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    multiple_birth = models.BooleanField(
        default=False,
        editable=False)

    objects = SubjectConsentManager()

    consent = ConsentManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.subject_identifier} V{self.version}'

    def save(self, *args, **kwargs):

        consent_version_cls = django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')

        if not self.version:
            try:
                consent_version_obj = consent_version_cls.objects.get(
                    screening_identifier=self.screening_identifier)
            except consent_version_cls.DoesNotExist:
                self.version = '4'
            else:
                self.version = consent_version_obj.version

        self.biological_caregiver = self.is_biological_mother()
        eligibility_criteria = ConsentEligibility(
            self.remain_in_study, self.hiv_testing, self.breastfeed_intent,
            self.consent_reviewed, self.citizen, self.study_questions,
            self.assessment_score, self.consent_signature, self.consent_copy,
            self.child_consent)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        if self.multiple_births in ['twins', 'triplets']:
            self.multiple_birth = True
        if self.is_eligible:
            if self.created and not self.subject_identifier:
                self.subject_identifier = self.update_subject_identifier_on_save()

            self.update_dataset_identifier()
            self.update_locator_subject_identifier()

        if self.caregiver_locator_obj:
            if not self.caregiver_locator_obj.first_name and not self.caregiver_locator_obj.last_name:
                self.caregiver_locator_obj.first_name = self.first_name
                self.caregiver_locator_obj.last_name = self.last_name
                self.caregiver_locator_obj.save()

        super().save(*args, **kwargs)

    def natural_key(self):
        return self.subject_identifier, self.version

    @property
    def multiple_births(self):
        """Returns value of births if the mother has twins/triplets.
        """
        dataset_cls = django_apps.get_model(
            'flourish_caregiver.maternaldataset')

        try:
            dataset_obj = dataset_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except dataset_cls.DoesNotExist:
            pass
        else:
            child_dataset_cls = django_apps.get_model(
                'flourish_child.childdataset')
            children = child_dataset_cls.objects.filter(
                study_maternal_identifier=dataset_obj.study_maternal_identifier)
            if children.count() == 2:
                return 'twins'
            elif children.count() == 3:
                return 'triplets'
            elif children.count() > 3:
                raise ValidationError(
                    'We do not expect more than triplets to exist.')
        return None

    @property
    def caregiver_type(self):
        """Return the letter that represents the caregiver type.
        """
        if self.biological_caregiver == 'Yes':
            return 'B'
        elif self.biological_caregiver == 'No':
            return 'C'
        return None

    def make_new_identifier(self):
        """Returns a new and unique identifier.

        Override this if needed.
        """
        if not self.is_eligible:
            return None
        subject_identifier = SubjectIdentifier(
            caregiver_type=self.caregiver_type,
            identifier_type='subject',
            requesting_model=self._meta.label_lower,
            site=self.site)
        return subject_identifier.identifier

    def update_dataset_identifier(self):
        dataset_cls = django_apps.get_model(
            'flourish_caregiver.maternaldataset')

        try:
            dataset_obj = dataset_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except dataset_cls.DoesNotExist:
            pass
        else:
            dataset_obj.subject_identifier = self.subject_identifier
            dataset_obj.save()

    def update_locator_subject_identifier(self):
        locator_cls = django_apps.get_model(
            'flourish_caregiver.caregiverlocator')
        try:
            locator_obj = locator_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except locator_cls.DoesNotExist:
            pass
        else:
            if not locator_obj.subject_identifier:
                locator_obj.subject_identifier = self.subject_identifier
                locator_obj.save()

    def is_biological_mother(self):
        # To refactor to include new enrollees !!
        prior_screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpriorbhpparticipants')
        preg_women_screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpregwomen')
        screening = None
        is_biological_mother = NO
        try:
            screening = prior_screening_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except prior_screening_cls.DoesNotExist:
            try:
                screening = preg_women_screening_cls.objects.get(
                    screening_identifier=self.screening_identifier)
            except preg_women_screening_cls.DoesNotExist:
                is_biological_mother = NO
            else:
                is_biological_mother = YES
        else:
            if (screening.mother_alive == YES and
                    screening.flourish_participation == 'interested'):
                is_biological_mother = YES
        return is_biological_mother

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

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('first_name')
        fields.append('last_name')
        return fields

    @property
    def caregiver_locator_model_cls(self):
        return django_apps.get_model(self.caregiver_locator_model)

    @property
    def caregiver_locator_obj(self):
        try:
            caregiver_locator = self.caregiver_locator_model_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except self.caregiver_locator_model_cls.DoesNotExist:
            return None
        else:
            return caregiver_locator

    class Meta(ConsentModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Adult Participation Consent'
        unique_together = (('subject_identifier', 'version'),
                           ('screening_identifier', 'version'),
                           ('subject_identifier', 'screening_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
