from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO

from ..maternal_choices import POS_NEG_IND


class MaternalHuuPreEnrollment(SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, ], )

    screening_identifier = models.CharField(
        verbose_name='Eligibility Identifier',
        max_length=36,
        unique=True,
        editable=False)

    maternal_dob = models.DateField(
        verbose_name='What is your DOB?', )

    child_hiv_docs = models.CharField(
        verbose_name='Is there documentation of the child’s HIV status?',
        choices=YES_NO,
        max_length=3, )

    child_hiv_result = models.CharField(
        verbose_name='HIV test result',
        choices=POS_NEG_IND,
        max_length=14)

    class Meta:
        app_label = 'flourish_maternal'
        verbose_name = 'Maternal HUU Pre-Enrollment'
        verbose_name_plural = 'Maternal HUU Pre-Enrollment'
