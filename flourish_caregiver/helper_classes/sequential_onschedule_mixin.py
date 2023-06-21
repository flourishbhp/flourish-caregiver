from django.apps import apps as django_apps
from edc_base import get_utcnow
from edc_visit_schedule import site_visit_schedules
from flourish_caregiver.helper_classes.schedule_dict import child_schedule_dict, caregiver_schedule_dict


class SeqEnrolOnScheduleMixin:
    def put_caregiver_onschedule(self):
        """Put a caregiver on schedule.
        """
        cohort = self.evaluated_cohort
        schedule_type = self.schedule_type
        child_count = str(self.child_consent_obj.caregiver_visit_count)

        # TODO: To get variables needed from the model
        onschedule_model = caregiver_schedule_dict[cohort][schedule_type][
            'onschedule_model']
        schedule_name = caregiver_schedule_dict[cohort][schedule_type][child_count]

        self.put_on_schedule(onschedule_model=onschedule_model,
                             schedule_name=schedule_name,
                             subject_identifier=self.caregiver_subject_identifier,
                             is_caregiver=True)

        prev_schedule_name = self.caregiver_last_qt_subject_schedule_obj.schedule_name

        self.delete_completed_appointments(
            appointment_model_cls=self.child_appointment_cls,
            subject_identifier=self.child_subject_identifier,
            prev_schedule_name=prev_schedule_name,
            new_schedule_name=schedule_name)

    def put_child_onschedule(self):

        cohort = self.evaluated_cohort
        schedule_type = self.schedule_type

        onschedule_model = child_schedule_dict[cohort][schedule_type]['onschedule_model']
        schedule_name = child_schedule_dict[cohort][schedule_type]['name']

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model,
            name=schedule_name)

        if not schedule.is_onschedule(subject_identifier=self.child_subject_identifier,
                                      report_datetime=self.child_consent_obj.consent_datetime):
            self.put_on_schedule(onschedule_model=onschedule_model,
                                 schedule_name=schedule_name,
                                 subject_identifier=self.child_subject_identifier)

            prev_schedule_name = self.child_last_qt_subject_schedule_obj.schedule_name

            self.delete_completed_appointments(
                appointment_model_cls=self.child_appointment_cls,
                subject_identifier=self.child_subject_identifier,
                prev_schedule_name=prev_schedule_name,
                new_schedule_name=schedule_name)

    def put_on_schedule(self, onschedule_model,
                        schedule_name, subject_identifier, is_caregiver=False):
        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model,
            name=schedule_name)
        schedule.put_on_schedule(
            subject_identifier=subject_identifier,
            onschedule_datetime=get_utcnow(),
            schedule_name=schedule_name)

        if is_caregiver:
            self.update_onschedule_model(onschedule_model=onschedule_model,
                                         schedule_name=schedule_name, schedule=schedule)

    def update_onschedule_model(self, onschedule_model, schedule_name, schedule):

        onschedule_model_cls = django_apps.get_model(onschedule_model)
        try:
            onschedule_model_cls.objects.get(
                subject_identifier=self.caregiver_subject_identifier,
                schedule_name=schedule_name,
                child_subject_identifier=self.child_subject_identifier)
        except onschedule_model_cls.DoesNotExist:
            try:
                onschedule_obj = schedule.onschedule_model_cls.objects.get(
                    subject_identifier=self.caregiver_subject_identifier,
                    schedule_name=schedule_name)
            except schedule.onschedule_model_cls.DoesNotExist:
                pass
            else:
                onschedule_obj.child_subject_identifier = self.child_subject_identifier
                onschedule_obj.save()

    @classmethod
    def delete_completed_appointments(cls, appointment_model_cls, subject_identifier,
                                      prev_schedule_name, new_schedule_name):
        """Deletes completed appointments from previous schedules which are present in
        new schedules.

        Args:
            appointment_model_cls (Type[Appointment]): Model class for Appointments.
            subject_identifier (str): Unique identifier for the subject.
            prev_schedule_name (str): Name of the previous schedule.
            new_schedule_name (str): Name of the new schedule.

        Returns:
            None
        """
        prev_appts = appointment_model_cls.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name=prev_schedule_name
        )

        new_appts = appointment_model_cls.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name=new_schedule_name
        )
        new_visit_codes = {appt.visit_code for appt in new_appts}
        for prev_appt in prev_appts:
            if prev_appt.visit_code in new_visit_codes:
                new_appt = new_appts.get(visit_code=prev_appt.visit_code)
                new_appt.delete()
