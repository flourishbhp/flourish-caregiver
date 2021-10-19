from django.apps import apps as django_apps
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_crypto_fields.fields import FirstnameField, LastnameField
from django_crypto_fields.fields import IdentityField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future, date_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_consent.field_mixins import PersonalFieldsMixin
from edc_consent.field_mixins import ReviewFieldsMixin, VerificationFieldsMixin
from edc_constants.choices import GENDER, YES_NO_NA, YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start

from ..choices import CHILD_IDENTITY_TYPE, COHORTS
from ..helper_classes.cohort import Cohort
from ..subject_identifier import InfantIdentifier
from .eligibility import CaregiverChildConsentEligibility
from .subject_consent import SubjectConsent

INFANT = 'infant'


class CaregiverChildConsent(SiteModelMixin, NonUniqueSubjectIdentifierFieldMixin,
                            IdentityFieldsMixin, ReviewFieldsMixin,
                            PersonalFieldsMixin, VerificationFieldsMixin, BaseUuidModel):

    """Inline table for caregiver's children"""

    subject_consent = models.ForeignKey(
        SubjectConsent,
        on_delete=models.PROTECT)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    first_name = FirstnameField(
        null=True, blank=True)

    last_name = LastnameField(
        verbose_name="Last name",
        null=True, blank=True)

    study_child_identifier = models.CharField(
        verbose_name='Previous study identifier',
        max_length=50,
        null=True,
        blank=True)

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER,
        max_length=1,
        null=True,
        blank=True)

    identity = IdentityField(
        verbose_name='Identity number',
        null=True,
        blank=True)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=CHILD_IDENTITY_TYPE,
        null=True,
        blank=True)

    confirm_identity = IdentityField(
        help_text='Retype the identity number',
        null=True,
        blank=True)

    child_dob = models.DateField(
        verbose_name="Date of birth",
        validators=[date_not_future, ],
        null=True,
        blank=True)

    child_test = models.CharField(
        verbose_name='Will you allow for HIV testing and counselling of '
                     'your Child',
        max_length=5,
        choices=YES_NO,
        help_text='If no, participant is not eligible.')

    child_remain_in_study = models.CharField(
        verbose_name='Is your child willing to remain in the study area until '
                     '2025?',
        max_length=5,
        choices=YES_NO,
        help_text='If no, participant is not eligible.')

    child_preg_test = models.CharField(
        verbose_name='If your child is female and will be 12 years or older '
                     'prior to 30-Jun-2025, will you allow the female child '
                     'to undergo pregnancy testing?',
        max_length=5,
        choices=YES_NO_NA,
        help_text='If no, participant is not eligible.')

    child_knows_status = models.CharField(
        verbose_name='If your child is ≥ 16 years, have they been told about '
                     'your HIV?',
        max_length=5,
        choices=YES_NO_NA,
        help_text='If no, participant is not eligible.')

    future_studies_contact = models.CharField(
        verbose_name=('Do you give us permission for us to contact you or your child'
                      ' for future studies?'),
        max_length=3,
        choices=YES_NO,)

    specimen_consent = models.CharField(
        verbose_name=('Do you give us permission for us to use your child\'s blood '
                      'samples for future studies?'),
        max_length=3,
        choices=YES_NO,)

    child_age_at_enrollment = models.DecimalField(
        decimal_places=2,
        max_digits=4)

    consent_datetime = models.DateTimeField(
        verbose_name='Consent date and time',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future])

    version = models.CharField(
        verbose_name='Consent version',
        max_length=10,
        help_text='See \'Consent Type\' for consent versions by period.',
        editable=False)

    cohort = models.CharField(
        max_length=12,
        choices=COHORTS,
        blank=True,
        null=True)

    caregiver_visit_count = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        blank=True,
        null=True)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    def save(self, *args, **kwargs):
        eligibility_criteria = CaregiverChildConsentEligibility(
            self.child_test, self.child_remain_in_study, self.child_preg_test,
            self.child_knows_status)
        self.version = self.subject_consent.consent_version
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        self.child_age_at_enrollment = (
            self.get_child_age_at_enrollment() if self.child_dob else 0)
        if self.is_eligible and not self.subject_identifier:
            self.subject_identifier = InfantIdentifier(
                maternal_identifier=self.subject_consent.subject_identifier,
                birth_order=self.birth_order,
                live_infants=self.live_infants,
                registration_status=self.registration_status,
                registration_datetime=self.consent_datetime,
                subject_type=INFANT,
                supplied_infant_suffix=self.subject_identifier_sufix).identifier


        super().save(*args, **kwargs)

    @property
    def live_infants(self):
        child_dummy_consent_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')
        return child_dummy_consent_cls.objects.filter(
            subject_identifier__icontains=self.subject_consent.subject_identifier).exclude(
                identity=self.identity).count() + 1

    @property
    def subject_identifier_sufix(self):

        caregiver_child_consent_cls = django_apps.get_model(self._meta.label_lower)
        child_identifier_postfix = ''
        if self.child_dataset:
            if self.subject_consent.multiple_birth:
                if (self.subject_consent.multiple_births == 'twins'
                        and self.child_dataset.twin_triplet):
                    twin_id = self.subject_consent.subject_identifier + '-' + '25'
                    try:
                        caregiver_child_consent_cls.objects.get(
                            subject_identifier=twin_id)
                    except caregiver_child_consent_cls.DoesNotExist:
                        child_identifier_postfix = '25'
                    else:
                        child_identifier_postfix = '35'
                elif (self.subject_consent.multiple_births == 'triplets'
                        and self.child_dataset.twin_triplet):
                    twin_id = self.subject_consent.subject_identifier + '-' + '36'
                    try:
                        caregiver_child_consent_cls.objects.get(
                            subject_identifier=twin_id)
                    except caregiver_child_consent_cls.DoesNotExist:
                        child_identifier_postfix = '36'
                    else:
                        twin_id = self.subject_consent.subject_identifier + '-' + '46'
                        try:
                            caregiver_child_consent_cls.objects.get(
                                subject_identifier=twin_id)
                        except caregiver_child_consent_cls.DoesNotExist:
                            child_identifier_postfix = '46'
                        else:
                            child_identifier_postfix = '56'
            else:
                children_count = caregiver_child_consent_cls.objects.filter(
                    subject_identifier__startswith=self.subject_consent.subject_identifier).exclude(
                        child_dob=self.child_dob,
                        first_name=self.first_name).count()
                if children_count:
                    child_identifier_postfix = str((children_count + 5) * 10)
                else:
                    child_identifier_postfix = 10
        else:
            children_count = caregiver_child_consent_cls.objects.filter(
                    subject_identifier__startswith=self.subject_consent.subject_identifier).exclude(
                        child_dob=self.child_dob,
                        first_name=self.first_name).count()
            if children_count:
                child_identifier_postfix = str((children_count + 5) * 10)
            else:
                child_identifier_postfix = 10
        return child_identifier_postfix

    @property
    def child_dataset(self):
        child_dataset_cls = django_apps.get_model('flourish_child.childdataset')
        try:
            child_dataset = child_dataset_cls.objects.get(
                study_child_identifier=self.study_child_identifier)
        except child_dataset_cls.DoesNotExist:
            pass
        else:
            return child_dataset
        return None

    @property
    def registration_status(self):
        return 'REGISTERED'

    @property
    def birth_order(self):
        caregiver_child_consent_cls = django_apps.get_model(self._meta.label_lower)
        return caregiver_child_consent_cls.objects.filter(
            subject_identifier__icontains=self.subject_consent.subject_identifier).exclude(
                identity=self.identity).count() + 1

    def get_child_age_at_enrollment(self):
        return Cohort().age_at_enrollment(
            child_dob=self.child_dob,
            check_date=self.created.date())

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Consent On Behalf Of Child'
        verbose_name_plural = 'Caregiver Consent On Behalf Of Child'
