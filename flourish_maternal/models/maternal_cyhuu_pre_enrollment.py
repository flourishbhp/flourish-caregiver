from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO

from ..maternal_choices import POS_NEG_IND


class MaternalCyhuuPreEnrollment(SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, ], )

    screening_identifier = models.CharField(
        verbose_name='Eligibility Identifier',
        max_length=36,
        unique=True,
        editable=False)

    biological_mother = models.CharField(
        verbose_name='Are you the biological mother of the child?',
        choices=YES_NO,
        max_length=3, )

    child_dob = models.DateField(
        verbose_name='What is the DOB of your child?', )

    hiv_docs = models.CharField(
        verbose_name='Do you have documentation of your HIV status?',
        choices=YES_NO,
        max_length=3, )

    hiv_test_result = models.CharField(
        verbose_name='HIV test result',
        choices=POS_NEG_IND,
        max_length=14)

    class Meta:
        app_label = 'flourish_maternal'
        verbose_name = 'Maternal CYHUU Pre-Enrollment'
        verbose_name_plural = 'Maternal CYHUU Pre-Enrollment'
