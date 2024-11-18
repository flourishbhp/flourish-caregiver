from django.conf import settings
from edc_appointment.creators import (
    UnscheduledAppointmentCreator as BaseUnscheduledAppointmentCreator)
from edc_model_wrapper import ModelWrapper


class AppointmentModelWrapper(ModelWrapper):

    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')

    @property
    def next_by_timepoint(self):
        """ Returns the previous appointment or None of all appointments
            for this subject for visit_code_sequence=0. Use this instead
            of attr defined on the base appointment model, to account for
            visit_schedule setup.
        """
        return self.model_cls.objects.filter(
            subject_identifier=self.subject_identifier,
            timepoint__gt=self.timepoint,
            visit_code_sequence=0,
            schedule_name=self.schedule_name
        ).order_by('timepoint').first()

    @property
    def next_visit_code_sequence(self):
        return getattr(self.object, 'next_visit_code_sequence', None)

    @property
    def appt_datetime(self):
        return getattr(self.object, 'appt_datetime', None)

    @property
    def timepoint_datetime(self):
        return getattr(self.object, 'timepoint_datetime', None)


class UnscheduledAppointmentCreator(BaseUnscheduledAppointmentCreator):

    @property
    def parent_appointment(self, check=True):
        if not self._parent_appointment:
            parent_appointment = super().parent_appointment
            self._parent_appointment = AppointmentModelWrapper(
                parent_appointment)
        return self._parent_appointment
