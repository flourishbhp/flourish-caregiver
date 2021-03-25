from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO, GENDER
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin

from ..choices import RELATION_TO_CHILD
from ..maternal_choices import POS_NEG_IND


class CaregiverPreviouslyEnrolled(UniqueSubjectIdentifierFieldMixin,
                                  SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, ], )

    maternal_prev_enroll = models.CharField(
        verbose_name='Is this caregiver the person '
                     'previously enrolled in a BHP study',
        choices=YES_NO,
        max_length=3, )

    current_hiv_status = models.CharField(
        verbose_name='What is your current HIV status?',
        choices=POS_NEG_IND,
        max_length=14,
        null=True,
        blank=True,)

    last_test_date = models.CharField(
        verbose_name='Do you know your last HIV test date?',
        choices=YES_NO,
        max_length=3,
        null=True,
        blank=True,)

    test_date = models.DateField(
        verbose_name='Test Date',
        null=True,
        blank=True,)

    is_date_estimated = models.CharField(
        verbose_name='Is this date estimated?',
        choices=YES_NO,
        max_length=3,
        null=True,
        blank=True,)

    sex = models.CharField(
        verbose_name='Gender',
        max_length=7,
        choices=GENDER,
        null=True,
        blank=True,)

    relation_to_child = models.CharField(
        verbose_name='Relationship to child',
        choices=RELATION_TO_CHILD,
        max_length=20,
        null=True,
        blank=True,)

    relation_to_child_other = OtherCharField()

    def __str__(self):
        return f'{self.subject_identifier}'

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Enrollment Information'
        verbose_name_plural = 'Caregiver Enrollment Information'
