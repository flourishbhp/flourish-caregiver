from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugModelMixin

from ..choices import CONSENT_VERSION


class TdConsentVersion(SiteModelMixin,
                       SearchSlugModelMixin, BaseUuidModel):

    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
        max_length=50,
        unique=True)

    version = models.CharField(
        verbose_name="Which version of the consent would you like to be consented with.",
        choices=CONSENT_VERSION,
        max_length=3)

    report_datetime = models.DateTimeField(
        verbose_name="Report datetime.",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ])

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'TD Consent Version'
        verbose_name_plural = 'TD Consent Version'
