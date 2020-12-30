from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_constants.choices import YES_NO

from .list_models import PhoneNumType
from ..choices import CONTACT_FAIL_REASON, CONTACT_MODE, HOME_VISIT_FAIL


class CaregiverContact(SiteModelMixin, BaseUuidModel):

    study_maternal_identifier = models.CharField(
        verbose_name='Study maternal Subject Identifier',
        max_length=50,
        unique=True)

    prev_study = models.CharField(
        verbose_name='Previous Study Name',
        max_length=100,)

    contact_date = models.DateField(
        verbose_name='Date of contact attempt')

    contact_mode = models.CharField(
        verbose_name='How was this person contacted?',
        max_length=100,
        choices=CONTACT_MODE)

    contact_mode_other = OtherCharField()

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
        choices=CONTACT_FAIL_REASON)

    alt_cell_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Cell phone (alternative)] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON)

    tel_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Telephone] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON)

    alt_tel_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Telephone (alternative)] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON)

    work_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Work Contact Number] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON)

    cell_alt_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Alternative contact person cell phone] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON)

    tel_alt_contact_fail = models.CharField(
        verbose_name='Why was the contact to [Alternative contact person telephone] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON)

    cell_resp_person_fail = models.CharField(
        verbose_name='Why was the contact to [Responsible person cell phone] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON)

    tel_resp_person_fail = models.CharField(
        verbose_name='Why was the contact to [Responsible person telephone] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON)

    home_visit_success = models.CharField(
        verbose_name='Was there a successful contact when visiting the household?',
        max_length=3,
        choices=YES_NO)

    home_visit_fail = models.CharField(
        verbose_name='Why was the household visit unsuccessful',
        max_length=100,
        choices=HOME_VISIT_FAIL)

    home_visit_fail_other = OtherCharField()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Enrollment Contact Attempt'
