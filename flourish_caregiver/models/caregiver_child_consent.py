from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models
from django_crypto_fields.fields import FirstnameField, LastnameField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future, date_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_constants.choices import GENDER, NOT_APPLICABLE, YES_NO_NA, YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start

from .eligibility import CaregiverChildConsentEligibility
from .subject_consent import SubjectConsent
from ..choices import CHILD_IDENTITY_TYPE, COHORTS
from ..helper_classes.cohort import Cohort


class CaregiverChildConsent(SiteModelMixin, NonUniqueSubjectIdentifierFieldMixin,
                            IdentityFieldsMixin, BaseUuidModel):
    """Inline table for caregiver's children"""

    subject_consent = models.ForeignKey(
        SubjectConsent,
        on_delete=models.PROTECT)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    first_name = FirstnameField()

    last_name = LastnameField()

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER,
        max_length=1)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=CHILD_IDENTITY_TYPE)

    child_dob = models.DateField(
        verbose_name="Date of birth",
        validators=[date_not_future, ])

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
        default=NOT_APPLICABLE,
        help_text='If no, participant is not eligible.')

    child_knows_status = models.CharField(
        verbose_name='If your child is ≥ 16 years, have they been told about '
                     'your HIV?',
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text='If no, participant is not eligible.')

    child_age_at_enrollment = models.DecimalField(
        decimal_places=2,
        max_digits=4)

    consent_datetime = models.DateTimeField(
        verbose_name='Consent date and time',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow)

    version = models.CharField(
        verbose_name='Consent version',
        max_length=10,
        help_text='See \'Consent Type\' for consent versions by period.',
        editable=False)

    cohort = models.CharField(
        max_length=12,
        choices=COHORTS,)

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
            self.get_child_age_at_enrollment() if self.child_dob else None)
        if self.is_eligible and not self.subject_identifier:
                self.subject_identifier = self.update_subject_identifier
        super().save(*args, **kwargs)

    @property
    def update_subject_identifier(self):

        child_dummy_consent_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')

        children_count = 1 + child_dummy_consent_cls.objects.filter(
            subject_identifier__icontains=self.subject_consent.subject_identifier).exclude(
                identity=self.identity).count()
        child_identifier_postfix = '-' + str(children_count * 10)
        return self.subject_consent.subject_identifier + child_identifier_postfix

    def get_child_age_at_enrollment(self):
        return Cohort().age_at_enrollment(
            child_dob=self.child_dob,
            check_date=self.created.date())

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Consent On Behalf Of Child'
        verbose_name_plural = 'Caregiver Consent On Behalf Of Child'
