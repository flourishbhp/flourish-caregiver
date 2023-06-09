from edc_visit_schedule import site_visit_schedules
from schedule_dict import child_schedule_dict, caregiver_schedule_dict


class OffScheduleSequentialCohortEnrollmentMixin:

    def take_off_child_offschedule(self):

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=self.child_last_qt_subject_schedule_obj.onschedule_model,
            name=self.child_last_qt_subject_schedule_obj.onschedule_model)

        if schedule.is_onschedule(subject_identifier=self.child_subject_identifier,
                                  report_datetime=self.child_consent_obj.consent_datetime):
            schedule.take_off_schedule(
                subject_identifier=self.child_subject_identifier,
                schedule_name=self.schedule_name)

    def take_off_caregiver_offschedule(self):

        cohort = self.evaluated_cohort
        schedule_type = self.schedule_type
        child_count = self.child_count

        schedule_name = caregiver_schedule_dict[cohort][schedule_type][child_count]

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=self.onschedule_model,
            name=self.schedule_name)

        if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                                  report_datetime=self.child_consent_obj.consent_datetime):
            schedule.take_off_schedule(
                subject_identifier=self.caregiver_subject_identifier,
                schedule_name=self.schedule_name)

    def take_off_schedule(self):
        self.take_off_caregiver_offschedule()
        self.take_off_child_offschedule()
