from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin

from ..choices import LOCATION_FOR_CONTACT, UNSUCCESSFUL_VISIT


class InPersonContactAttempt(SiteModelMixin, BaseUuidModel):

    study_maternal_identifier = models.CharField(
        verbose_name='Study maternal Subject Identifier',
        max_length=50,
        unique=True)

    prev_study = models.CharField(
        verbose_name='Previous Study Name',
        max_length=100, )

    contact_date = models.DateField(
        verbose_name='Date of contact attempt')

    contact_location = models.CharField(
        verbose_name='Which location was used for contact?',
        max_length=100,
        null=True,
        choices=LOCATION_FOR_CONTACT)

    successful_location = models.CharField(
        verbose_name='Which location(s) were successful?',
        max_length=100,
        blank=True,
        null=True,
        choices=LOCATION_FOR_CONTACT)

    phy_addr_unsuc = models.CharField(
        verbose_name='Why was the in-person visit to [Physical Address with '
                     'detailed description] unsuccessful',
        max_length=100,
        blank=True,
        null=True,
        choices=UNSUCCESSFUL_VISIT)

    phy_addr_unsuc_other = models.CharField(
        max_length=50,
        verbose_name='Visit unsuccessful other',
        blank=True,
        null=True)

    workplace_unsuc = models.CharField(
        verbose_name='Why was the in-person visit to [Name and location of '
                     'workplace] unsuccessful',
        max_length=100,
        blank=True,
        null=True,
        choices=UNSUCCESSFUL_VISIT)

    workplace_unsuc_other = models.CharField(
        max_length=50,
        verbose_name='Unsuccessful visit reason other',
        blank=True,
        null=True)

    contact_person_unsuc = models.CharField(
        verbose_name='Why was the in-person visit to Contact person [Full '
                     'physical address] unsuccessful',
        max_length=100,
        blank=True,
        null=True,
        choices=UNSUCCESSFUL_VISIT)

    contact_person_unsuc_other = models.CharField(
        max_length=50,
        verbose_name='Visit to Contact person unsuccessful other',
        blank=True,
        null=True)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'In Person Contact Attempt'
        verbose_name_plural = 'In Person Contact Attempt'
