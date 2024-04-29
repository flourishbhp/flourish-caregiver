from django.db import models

from edc_base.model_validators import datetime_not_future
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_protocol.validators import datetime_not_before_study_start
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin

from ...maternal_choices import CONTACT_TYPE


class CaregiverContactFieldsMixin(NonUniqueSubjectIdentifierFieldMixin,
                                  BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Date',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    contact_type = models.CharField(
        verbose_name='Type of contact',
        choices=CONTACT_TYPE,
        max_length=25,
    )

    contact_datetime = models.DateTimeField(
        verbose_name='Contact datetime',
        validators=[datetime_not_future, datetime_not_before_study_start],
        help_text='This date can be modified.')

    contact_success = models.CharField(
        verbose_name='Were you able to reach the participant?',
        max_length=5,
        choices=YES_NO
    )

    class Meta:
        abstract = True
