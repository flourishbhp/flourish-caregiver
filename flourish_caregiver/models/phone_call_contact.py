from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin

from .list_models import PhoneNumType
from ..choices import CONTACT_FAIL_REASON


class PhoneCallContact(SiteModelMixin, BaseUuidModel):

    study_maternal_identifier = models.CharField(
        verbose_name='Study maternal Subject Identifier',
        max_length=50,
        unique=True)

    prev_study = models.CharField(
        verbose_name='Previous Study Name',
        max_length=100,)

    contact_date = models.DateField(
        verbose_name='Date of contact attempt')

    phone_num_type = models.ManyToManyField(
        PhoneNumType,
        related_name='phonenumtype',
        verbose_name='Which phone number(s) was used for contact?')

    phone_num_success = models.ManyToManyField(
        PhoneNumType,
        related_name='phonenumsuccess',
        verbose_name='Which number(s) were you successful in reaching?')

    cell_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Cell phone] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        blank=True,
        null=True)

    alt_cell_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Cell phone (alternative)] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        blank=True,
        null=True)

    tel_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Telephone] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        blank=True,
        null=True)

    alt_tel_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Telephone (alternative)] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        blank=True,
        null=True)

    work_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Work Contact Number] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        blank=True,
        null=True)

    cell_alt_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Alternative contact person cell phone] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        blank=True,
        null=True)

    tel_alt_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Alternative contact person telephone] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        blank=True,
        null=True)

    cell_resp_person_fail = models.CharField(
        verbose_name='Why was the contact to [Responsible person cell phone] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        blank=True,
        null=True)

    tel_resp_person_fail = models.CharField(
        verbose_name='Why was the contact to [Responsible person telephone] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        blank=True,
        null=True)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Phone Call Contact Attempt'
