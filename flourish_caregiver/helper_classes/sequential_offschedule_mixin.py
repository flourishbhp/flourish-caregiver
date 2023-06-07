from edc_visit_schedule import site_visit_schedules


class OffScheduleSequentialCohortEnrollmentMixin:

    def take_off_child_offschedule(self):
        if 'quartarly' in self.name and self.subject_type:
            _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                onschedule_model=self.onschedule_model,
                name=self.schedule_name)

            if schedule.is_onschedule(subject_identifier=self.child_subject_identifier,
                                      report_datetime=self.child_consent_obj.consent_datetime):
                schedule.take_off_schedule(
                    subject_identifier=self.child_subject_identifier,
                    schedule_name=self.schedule_name)

    def take_off_caregiver_offschedule(self):

        if 'quartarly' in self.name and self.subject_type:
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
