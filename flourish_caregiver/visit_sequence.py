from django.apps import apps as django_apps
from django.db.models import Q
from edc_visit_tracking.visit_sequence import VisitSequence, VisitSequenceError

from .helper_classes.utils import get_previous_by_appt_datetime


class VisitSequence(VisitSequence):
    def __init__(self, appointment=None):
        self.appointment = appointment
        self.appointment_model_cls = self.appointment.__class__
        self.model_cls = getattr(
            self.appointment_model_cls,
            self.appointment_model_cls.related_visit_model_attr()
        ).related.related_model
        self.subject_identifier = self.appointment.subject_identifier
        self.visit_schedule_name = self.appointment.visit_schedule_name
        self.visit_code = self.appointment.visit_code
        previous_visit = self.appointment.schedule.visits.previous(
            self.visit_code)
        self.previous_appointment = get_previous_by_appt_datetime(self.appointment)

        try:
            self.previous_visit_code = getattr(
                self.previous_appointment, 'visit_code', None) or previous_visit.code
        except AttributeError:
            self.previous_visit_code = None
        self.sequence_query = Q()
        if self.visit_code == self.previous_visit_code:
            previous_visit_code_sequence = getattr(
                self.previous_appointment, 'visit_code_sequence', 0)
            self.sequence_query = Q(visit_code_sequence=previous_visit_code_sequence)
        self.previous_visit_missing = self.previous_visit_code and not self.previous_visit

    @property
    def exclude_visit_codes(self):
        return ['2002S']

    def enforce_sequence(self):
        if (self.previous_visit_missing and self.visit_code not in
                self.exclude_visit_codes):
            raise VisitSequenceError(
                'Previous visit report required. Enter report for '
                f'\'{self.previous_visit_code}\' before completing this report.')

    @property
    def previous_visit(self):
        if not self.previous_visit_code:
            return None

        prev_visit = self.get_previous_visit()
        return prev_visit if prev_visit else self.get_previous_visit_by_appt()

    def get_previous_visit(self):
        try:
            return self.model_cls.objects.get(
                appointment__subject_identifier=self.subject_identifier,
                visit_schedule_name=self.visit_schedule_name,
                schedule_name=self.appointment.schedule_name,
                visit_code=self.previous_visit_code
            )
        except self.model_cls.DoesNotExist:
            return None

    def get_previous_visit_by_appt(self):
        """
        Returns the previous visit by an appointment if the visit code does not exist
        in the exclude visit codes
        """
        prev_visit = None

        if self.visit_code not in self.exclude_visit_codes:
            prev_appointment = self.get_previous_appointment()

            if prev_appointment:
                prev_visit = self.get_visit_for_appointment(prev_appointment)

            elif self.previous_appointment:
                prev_visit = getattr(
                    self.previous_appointment, self.model_cls._meta.model_name, None)
            else:
                try:
                    prev_visit = self.model_cls.objects.get(
                        subject_identifier=self.get_prev_onschedule_obj
                        .subject_identifier,
                        visit_schedule_name=self.visit_schedule_name,
                        schedule_name=self.appointment.schedule_name,
                        visit_code=self.previous_visit_code)
                except self.model_cls.DoesNotExist:
                    pass

        return prev_visit

    def get_previous_appointment(self):
        return self.appointment_model_cls.objects.filter(
            self.sequence_query,
            subject_identifier=self.subject_identifier,
            visit_code=self.previous_visit_code).order_by(
            '-visit_code_sequence').first()

    def get_visit_for_appointment(self, appointment):
        try:
            return self.model_cls.objects.get(appointment=appointment)
        except self.model_cls.DoesNotExist:
            return None

    @property
    def get_prev_onschedule_obj(self):
        onschedule_model = getattr(
            self.appointment.schedule, 'onschedule_model', None)
        onschedule_model_cls = django_apps.get_model(onschedule_model)
        try:
            onschedule_obj = onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                schedule_name=self.appointment.schedule_name)
        except onschedule_model_cls.DoesNotExist:
            return None
        else:
            prev_onschedule_obj = onschedule_model_cls.objects.filter(
                child_subject_identifier=onschedule_obj.child_subject_identifier,
                schedule_name=self.appointment.schedule_name)
            return prev_onschedule_obj.earliest(
                'onschedule_datetime') if prev_onschedule_obj.exists() else None
