from django.db import models
from edc_base import get_utcnow
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future, date_not_future
from edc_identifier.managers import SubjectIdentifierManager
from edc_protocol.validators import datetime_not_before_study_start, \
    date_not_before_study_start

from edc_action_item.model_mixins import ActionModelMixin
from edc_visit_schedule.model_mixins import OffScheduleModelMixin
from flourish_prn.choices import CAREGIVER_OFF_STUDY_REASON

from ..action_items import TB_OFF_STUDY_ACTION


class TbOffStudy(OffScheduleModelMixin, ActionModelMixin, BaseUuidModel):

    action_name = TB_OFF_STUDY_ACTION

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use'
                   ' the date/time this information was reported.'))

    reason = models.CharField(
        verbose_name=('Please code the primary reason participant taken'
                      ' off-study'),
        max_length=115,
        choices=CAREGIVER_OFF_STUDY_REASON)

    offstudy_date = models.DateField(
        verbose_name="Off-study Date",
        validators=[
            date_not_before_study_start,
            date_not_future])

    reason_other = OtherCharField()

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment",
        blank=True,
        null=True)

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def take_off_schedule(self):
        pass

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Off Study'
        verbose_name_plural = 'TB Off Study'
