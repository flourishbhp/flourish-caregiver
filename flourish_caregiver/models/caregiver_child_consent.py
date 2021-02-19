from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_registration.model_mixins import (
    UpdatesOrCreatesRegistrationModelMixin)
from edc_search.model_mixins import SearchSlugManager

from edc_consent.field_mixins import IdentityFieldsMixin, CitizenFieldsMixin
from edc_consent.field_mixins import (PersonalFieldsMixin, ReviewFieldsMixin,
                                      VulnerabilityFieldsMixin)
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from .model_mixins import SearchSlugModelMixin

from ..choices import IDENTITY_TYPE, COHORTS


class CaregiverChildConsentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier, version):
        return self.get(
            subject_identifier=subject_identifier, version=version)


class CaregiverChildConsent(
        ConsentModelMixin, SiteModelMixin,
        UpdatesOrCreatesRegistrationModelMixin,
        NonUniqueSubjectIdentifierModelMixin, IdentityFieldsMixin,
        ReviewFieldsMixin, PersonalFieldsMixin,
        VulnerabilityFieldsMixin, CitizenFieldsMixin,
        SearchSlugModelMixin, BaseUuidModel):

    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
        max_length=50)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=IDENTITY_TYPE)

    child_test = models.CharField(
        verbose_name='Will you allow for HIV testing and counselling of '
                     'your Child',
        max_length=5,
        choices=YES_NO)

    remain_in_study = models.CharField(
        verbose_name='Are you willing to remain in the study area for 5 years?',
        max_length=5,
        choices=YES_NO)

    child_preg_test = models.CharField(
        verbose_name='If your child is female and will be 12 years or older '
                     'prior to 30-Jun-2025, will you allow the female child '
                     'to undergo pregnancy testing?',
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

    consent = ConsentManager()

    history = HistoricalRecords()

    objects = CaregiverChildConsentManager()

    def __str__(self):
        return f'{self.subject_identifier} V{self.version}'

    def natural_key(self):
        return (self.subject_identifier, self.version)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.extend(['identity', 'screening_identifier',
                       'first_name', 'last_name'])
        return fields

    class Meta(ConsentModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Consent for Child Participation'
        verbose_name_plural = 'Caregiver Consent for Child Participation'
        unique_together = (('subject_identifier', 'version'),
                           ('subject_identifier', 'screening_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
