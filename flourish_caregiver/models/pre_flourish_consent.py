import re
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_consent.field_mixins import (
    CitizenFieldsMixin, VulnerabilityFieldsMixin)
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_consent.field_mixins import ReviewFieldsMixin, PersonalFieldsMixin
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.constants import UUID_PATTERN
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_search.model_mixins import SearchSlugManager

from ..choices import IDENTITY_TYPE
from ..subject_identifier import PreFlourishIdentifier
from ..maternal_choices import RECRUIT_SOURCE, RECRUIT_CLINIC
from .model_mixins import SearchSlugModelMixin


class PreFlourishConsentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, pre_flourish_identifier, version):
        return self.get(
            pre_flourish_identifier=pre_flourish_identifier, version=version)


class PreFlourishConsent(
        ConsentModelMixin, SiteModelMixin,
        UpdatesOrCreatesRegistrationModelMixin, IdentityFieldsMixin,
        ReviewFieldsMixin, PersonalFieldsMixin, CitizenFieldsMixin,
        VulnerabilityFieldsMixin, SearchSlugModelMixin, BaseUuidModel):

    subject_screening_model = 'flourish_caregiver.subjectscreening'

    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
        max_length=50)

    pre_flourish_identifier = models.CharField(
        verbose_name="Pre-Flourish Identifier",
        max_length=50)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=IDENTITY_TYPE)

    recruit_source = models.CharField(
        max_length=75,
        choices=RECRUIT_SOURCE,
        verbose_name=("The participant first learned about the flourish study "
                      "from "))

    recruit_source_other = OtherCharField(
        max_length=35,
        verbose_name="if other recruitment source, specify...",
        blank=True,
        null=True)

    recruitment_clinic = models.CharField(
        max_length=100,
        verbose_name="The participant was recruited from",
        choices=RECRUIT_CLINIC)

    recruitment_clinic_other = models.CharField(
        max_length=100,
        verbose_name="if other recruitment clinic, specify...",
        blank=True,
        null=True,)

    objects = PreFlourishConsentManager()

    consent = ConsentManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.pre_flourish_identifier} V{self.version}'

    def natural_key(self):
        return (self.pre_flourish_identifier, self.version)

    def save(self, *args, **kwargs):
        if not self.id:
            self.pre_flourish_identifier = self.update_pre_flourish_identifier_on_save()

    def update_pre_flourish_identifier_on_save(self):
        """Returns a pre_flourish_identifier if not already set.
        """
        if not self.pre_flourish_identifier:
            self.pre_flourish_identifier = self.make_new_identifier()
        elif re.match(UUID_PATTERN, self.pre_flourish_identifier):
            self.subject_identifier = self.make_new_identifier()
        return self.pre_flourish_identifier

    def make_new_identifier(self):
        """Returns a new and unique identifier.

        Override this if needed.
        """
        pre_flourish_identifier = PreFlourishIdentifier(
            identifier_type='subject',
            requesting_model=self._meta.label_lower,
            site=self.site)
        return pre_flourish_identifier.identifier

    @property
    def consent_version(self):
        return self.version

    class Meta(ConsentModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Pre Flourish Consent'
        unique_together = (('pre_flourish_identifier', 'version'),
                           ('pre_flourish_identifier', 'screening_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
