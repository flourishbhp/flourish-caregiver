from django.core.validators import RegexValidator
from django.db import models
from django_crypto_fields.fields import EncryptedCharField, FirstnameField, LastnameField
from edc_base.model_fields import IsDateEstimatedField
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.field_mixins import IdentityFieldsMixin, CitizenFieldsMixin, ReviewFieldsMixin
from edc_consent.field_mixins import PersonalFieldsMixin, VulnerabilityFieldsMixin
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_consent.validators import eligible_if_yes
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_search.model_mixins import SearchSlugManager
from edc_constants.choices import GENDER
from ..choices import GENDER_OTHER
from ..choices import IDENTITY_TYPE
from .model_mixins import SearchSlugModelMixin




class TbAdolConsentManager(ConsentManager, SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier, version):
        return self.get(
            subject_identifier=subject_identifier, version=version)
        
class TbAdolConsent(ConsentModelMixin, SiteModelMixin,
                    UpdatesOrCreatesRegistrationModelMixin,
                    NonUniqueSubjectIdentifierModelMixin, IdentityFieldsMixin,
                    PersonalFieldsMixin, VulnerabilityFieldsMixin, CitizenFieldsMixin,
                    ReviewFieldsMixin, SearchSlugModelMixin, BaseUuidModel):

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

    is_dob_estimated = IsDateEstimatedField(
        verbose_name="Is the caregiver date of birth estimated?",
        null=True,
        blank=False)

    tb_blood_test_consent = models.CharField(
        verbose_name=('Will you allow for blood testing for TB for your adolescent? '),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text='Participant is not eligible if no')

    future_studies_contact = models.CharField(
        verbose_name=('Contact for future studies: Do you give us permission for us '
                      'to contact you or your child for future studies?'),
        max_length=3,
        choices=YES_NO)

    samples_future_studies = models.CharField(
        verbose_name=('Use of Samples in Future Research: Do you give us permission to use '
                      'your child\'s blood samples for future studies?'),
        max_length=3,
        choices=YES_NO)

    is_eligible = models.BooleanField(
        default=True,
        editable=False)

    gender_other = OtherCharField()

    objects = TbAdolConsentManager()

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
        verbose_name = 'TB Adolescent Caregiver Consent'
        unique_together = (
            ('subject_identifier', 'version'),
            ('first_name', 'dob', 'initials', 'version'))



class TbAdolChildConsent(BaseUuidModel):
    
    tb_adol_consent = models.ForeignKey(TbAdolConsent, on_delete=models.PROTECT)
    
    subject_identifier = models.CharField(verbose_name='Subject Identifer', max_length=20)
    
    adol_firstname = FirstnameField(
        verbose_name = 'Adolescent Firstname',
        blank=False,
        max_length = 50,)
    
    adol_lastname = LastnameField(
        verbose_name='Adolescent Lastname',
        blank=False,
        max_length = 50,)
    
    adol_gender = models.CharField(
        verbose_name='Adolescent Gender',
        choices=GENDER,
        max_length=1)
    
    adol_dob = models.DateField(
        verbose_name='Adolescent DOB'
    )
    
    def natural_key(self):
        return self.subject_identifier, self.version
    
    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Adolescent Child Consent'
        unique_together = (
            ('adol_firstname', 'adol_lastname', 'adol_dob', 'adol_gender'))
