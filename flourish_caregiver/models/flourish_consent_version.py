from django.apps import apps as django_apps
from django.db import models
from django.utils import timezone
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future, datetime_is_future
from edc_base.sites import SiteModelMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugModelMixin

from ..choices import CHILD_CONSENT_VERSION, CONSENT_VERSION

caregiver_config = django_apps.get_app_config('flourish_caregiver')


class FlourishConsentVersion(SiteModelMixin, SearchSlugModelMixin,
                             BaseUuidModel):
    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
        max_length=50,
        unique=True)

    version = models.CharField(
        verbose_name="Which version of the consent would you like to be consented with?",
        choices=CONSENT_VERSION,
        max_length=3)

    child_version = models.CharField(
        verbose_name=(
            "Which version of the consent would you like to consent on behalf of "
            "your child with?"),
        choices=CHILD_CONSENT_VERSION,
        max_length=3,
        default=str(caregiver_config.child_consent_version),
        null=True,
        blank=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report datetime.",
        default=timezone.now,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
            datetime_is_future
        ])

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Flourish Consent Version'
        verbose_name_plural = 'Flourish Consent Version'
