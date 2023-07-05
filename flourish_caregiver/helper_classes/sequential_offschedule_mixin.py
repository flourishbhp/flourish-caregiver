from edc_base.utils import get_utcnow
from edc_visit_schedule import site_visit_schedules


class OffScheduleSequentialCohortEnrollmentMixin:

    def take_off_child_offschedule(self):

        schedule_name = self.child_last_qt_subject_schedule_obj.schedule_name
        onschedule_model = self.child_last_qt_subject_schedule_obj.onschedule_model

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model,
            name=schedule_name)

        if schedule.is_onschedule(subject_identifier=self.child_subject_identifier,
                                  report_datetime=get_utcnow()):
            schedule.take_off_schedule(
                subject_identifier=self.child_subject_identifier,
                schedule_name=schedule_name)

    def take_off_caregiver_offschedule(self):

        schedule_name = self.caregiver_last_qt_subject_schedule_obj.schedule_name
        onschedule_model = self.caregiver_last_qt_subject_schedule_obj.onschedule_model

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model,
            name=schedule_name)

        if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                                  report_datetime=get_utcnow()):
            schedule.take_off_schedule(
                subject_identifier=self.caregiver_subject_identifier,
                schedule_name=schedule_name)

    def take_off_schedule(self):
        self.take_off_caregiver_offschedule()
        self.take_off_child_offschedule()
