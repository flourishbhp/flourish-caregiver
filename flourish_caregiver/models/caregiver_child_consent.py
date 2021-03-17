from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_constants.choices import (GENDER_UNDETERMINED, NOT_APPLICABLE,
                                   YES_NO_NA)
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin

from .subject_consent import SubjectConsent
from ..choices import IDENTITY_TYPE


class CaregiverChildConsent(NonUniqueSubjectIdentifierModelMixin,
                            IdentityFieldsMixin, BaseUuidModel):
    """Inline table for caregiver's children"""

    subject_consent = models.ForeignKey(
        SubjectConsent,
        on_delete=models.PROTECT)

    first_name = models.CharField(
        max_length=50,
        null=True, blank=True)

    last_name = models.CharField(
        verbose_name="Last name",
        max_length=50,
        null=True, blank=True)

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER_UNDETERMINED,
        max_length=1,
        null=True,
        blank=True)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=IDENTITY_TYPE)

    child_dob = models.DateField(
        verbose_name="Date of birth",
        null=True,
        blank=True)

    child_test = models.CharField(
        verbose_name='Will you allow for HIV testing and counselling of '
                     'your Child',
        max_length=5,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE)

    child_remain_in_study = models.CharField(
        verbose_name='Is your child willing to remain in the study area until '
                     '2025?',
        max_length=5,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE)

    child_preg_test = models.CharField(
        verbose_name='If your child is female and will be 12 years or older '
                     'prior to 30-Jun-2025, will you allow the female child '
                     'to undergo pregnancy testing?',
        max_length=5,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE)

    child_knows_status = models.CharField(
        verbose_name='If your child is ≥ 16 years, have they been told about '
                     'your HIV?',
        max_length=5,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Consent On Behalf Of Child'
        verbose_name_plural = 'Caregiver Consent On Behalf Of Child'
