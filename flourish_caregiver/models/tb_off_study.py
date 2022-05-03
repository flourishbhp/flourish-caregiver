from django.db import models
from edc_base import get_utcnow
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_validators import datetime_not_future, date_not_future
from edc_protocol.validators import datetime_not_before_study_start, \
    date_not_before_study_start
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from flourish_caregiver.models.model_mixins import CrfModelMixin
from flourish_prn.choices import CAREGIVER_OFF_STUDY_REASON, OFFSTUDY_POINT
from . import CaregiverOffSchedule


class TbOffStudy(CrfModelMixin, OffScheduleModelMixin):
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

    offstudy_point = models.CharField(
        verbose_name='At what point did the mother go off study',
        choices=OFFSTUDY_POINT,
        max_length=50,
        blank=True, null=True,
        help_text='For pregnant women enrolled in Cohort A')

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

    history = HistoricalRecords()

    def take_off_schedule(self):
        off_schedule_obj = CaregiverOffSchedule.objects.create(
            subject_identifier=self.maternal_visit.subject_identifier,
            offschedule_datetime=self.report_datetime,
            schedule_name='tb_2_months_schedule')
        off_schedule_obj.save()


    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Off Study'
        verbose_name_plural = 'TB Off Study'
