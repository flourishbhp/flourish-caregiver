from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO

from ..choices import RELATION_TO_CHILD
from ..maternal_choices import POS_NEG_IND


class CaregiverPreviouslyEnrolled(SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, ], )

    screening_identifier = models.CharField(
        verbose_name='Eligibility Identifier',
        max_length=36,
        unique=True,
        editable=False)

    maternal_prev_enroll = models.CharField(
        verbose_name='Is this caregiver the person '
                     'previously enrolled in a BHP study',
        choices=YES_NO,
        max_length=3, )

    current_hiv_status = models.CharField(
        verbose_name='What is your current HIV status?',
        choices=POS_NEG_IND,
        max_length=14)

    last_test_date = models.DateField(
        verbose_name='Do you know your last HIV test date?',
        choices=YES_NO,
        max_length=3, )

    test_date = models.DateField(
        verbose_name='Test Date', )

    is_date_estimated = models.CharField(
        verbose_name='Is this date estimated?',
        choices=YES_NO,
        max_length=3, )

    dob = models.DateField(
        verbose_name="Date of birth",
        null=True,
        blank=True,
        validators=[datetime_not_future, ],)

    sex = models.CharField(
        verbose_name='Gender',
        max_length=7)

    relation_to_child = models.CharField(
        verbose_name='Relationship to child',
        choices=RELATION_TO_CHILD,
        max_length=20, )

    relation_to_child_other = OtherCharField()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Previous Caregivers Enrollment'
        verbose_name_plural = 'Previous Caregivers Enrollment'
