from django.apps import apps as django_apps
from django.db import transaction
from edc_visit_tracking.visit_sequence import VisitSequence


class VisitSequence(VisitSequence):
    """ Override property for previous_visit for sequential enrollment
        or participant's replacing others, appointments continuing off
        where the previous onschedule appts were last done.
    """

    @property
    def previous_visit(self):
        """Returns the previous visit model instance if it exists.
        """
        previous_visit = None
        if self.previous_visit_code:
            with transaction.atomic():
                try:
                    previous_visit = self.model_cls.objects.get(
                        appointment__subject_identifier=self.subject_identifier,
                        visit_schedule_name=self.visit_schedule_name,
                        schedule_name=self.appointment.schedule_name,
                        visit_code=self.previous_visit_code)
                except Exception:
                    previous_appointment = self.appointment_model_cls.objects.filter(
                        subject_identifier=self.subject_identifier,
                        visit_code=self.previous_visit_code).order_by(
                            '-visit_code_sequence').first()
                    if previous_appointment:
                        previous_visit = self.model_cls.objects.get(
                            appointment=previous_appointment)
                    else:
                        subject_identifier = getattr(
                            self.get_prev_onschedule_obj, 'subject_identifier', None)
                        try:
                            previous_visit = self.model_cls.objects.get(
                                subject_identifier=subject_identifier,
                                visit_schedule_name=self.visit_schedule_name,
                                schedule_name=self.appointment.schedule_name,
                                visit_code=self.previous_visit_code)
                        except self.model_cls.DoesNotExist:
                            previous_visit = None
        return previous_visit

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
            if prev_onschedule_obj.exists():
                return prev_onschedule_obj.earliest('onschedule_datetime')
