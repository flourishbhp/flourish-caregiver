from django.core.validators import RegexValidator
from django.db import models
from django_crypto_fields.fields import EncryptedCharField
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_consent.field_mixins import PersonalFieldsMixin, VulnerabilityFieldsMixin
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_consent.validators import eligible_if_yes
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_search.model_mixins import SearchSlugManager

from ..choices import GENDER_OTHER
from ..choices import IDENTITY_TYPE
from .model_mixins import SearchSlugModelMixin


class InformedConsentManager(ConsentManager, SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier, version):
        return self.get(
            subject_identifier=subject_identifier, version=version)


class TbInformedConsent(ConsentModelMixin, SiteModelMixin,
                        UpdatesOrCreatesRegistrationModelMixin,
                        NonUniqueSubjectIdentifierModelMixin, IdentityFieldsMixin,
                        PersonalFieldsMixin, VulnerabilityFieldsMixin,
                        SearchSlugModelMixin, BaseUuidModel):
    subject_screening_model = 'flourish_caregiver.subjectscreening'

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters '
                     'only in upper case, no spaces.'))],
        help_text=('Ensure initials consist of letters '
                   'only in upper case, no spaces.'),
        null=True, blank=False)

    consent_datetime = models.DateTimeField(
        verbose_name='Consent date and time',
        help_text='Date and time of consent.',
        null=True)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=30,
        choices=IDENTITY_TYPE)

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER_OTHER,
        max_length=5,
        null=True,
        blank=False)

    consent_to_participate = models.CharField(
        verbose_name='Do you consent to participate in the study?',
        choices=YES_NO,
        max_length=3,
        validators=[eligible_if_yes, ],
        help_text='If no, participant is not eligible.')

    is_eligible = models.BooleanField(
        default=True,
        editable=False)

    gender_other = OtherCharField()

    objects = InformedConsentManager()

    consent = ConsentManager()

    on_site = CurrentSiteManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.subject_identifier} V{self.version}'

    def natural_key(self):
        return self.subject_identifier, self.version

    def save(self, *args, **kwargs):
        self.version = '1'
        super().save(*args, **kwargs)

    @property
    def consent_version(self):
        return self.version

    class Meta(ConsentModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Informed Consent'
        verbose_name_plural = 'TB Informed Consent'
        unique_together = (
            ('subject_identifier', 'version'),
            ('first_name', 'dob', 'initials', 'version'))
