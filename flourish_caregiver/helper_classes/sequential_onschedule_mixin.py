from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.db.models import Q
from edc_appointment.models import Appointment
from edc_appointment.constants import NEW_APPT
from edc_base import get_utcnow
from edc_visit_schedule import site_visit_schedules
from flourish_caregiver.helper_classes.schedule_dict import child_schedule_dict, \
    caregiver_schedule_dict
from flourish_child.models import Appointment as ChildAppointment


class SeqEnrolOnScheduleMixin:

    def put_caregiver_onschedule(self):
        """Put a caregiver on schedule.
        """
        cohort = self.evaluated_cohort
        schedule_type = self.schedule_type
        child_count = str(self.child_consent_obj.caregiver_visit_count)
        onschedule_datetime = self.caregiver_last_qt_subject_schedule_obj.onschedule_datetime

        # TODO: To get variables needed from the model
        onschedule_model = caregiver_schedule_dict[cohort][schedule_type][
            'onschedule_model']
        schedule_name = caregiver_schedule_dict[cohort][schedule_type][child_count]


        self.put_on_schedule(onschedule_model=onschedule_model,
                                schedule_name=schedule_name,
                                onschedule_datetime=onschedule_datetime,
                                subject_identifier=self.caregiver_subject_identifier,
                                is_caregiver=True)

        self.delete_completed_appointments(
            appointment_model_cls=Appointment,
            subject_identifier=self.caregiver_subject_identifier,
            schedule_name=schedule_name)

        if 'follow' in schedule_type:

            fu_onschedule_model =  caregiver_schedule_dict[cohort]['followup']['onschedule_model']
            fu_schedule_name =  caregiver_schedule_dict[cohort]['followup'][child_count]
            base_appt_datetime = get_utcnow() + relativedelta(months=6)

            self.put_on_schedule(onschedule_model=fu_onschedule_model,
                                schedule_name=fu_schedule_name,
                                base_appt_datetime=base_appt_datetime,
                                subject_identifier=self.caregiver_subject_identifier,
                                is_caregiver=True)

    def put_child_onschedule(self):

        cohort = self.evaluated_cohort
        schedule_type = self.schedule_type

        onschedule_model = child_schedule_dict[cohort][schedule_type]['onschedule_model']
        schedule_name = child_schedule_dict[cohort][schedule_type]['name']
        onschedule_datetime = self.child_last_qt_subject_schedule_obj.onschedule_datetime


        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model,
            name=schedule_name)

        if not schedule.is_onschedule(subject_identifier=self.child_subject_identifier,
                                      report_datetime=onschedule_datetime):
            self.put_on_schedule(onschedule_model=onschedule_model,
                                 schedule_name=schedule_name,
                                 base_appt_datetime=onschedule_datetime,
                                 subject_identifier=self.child_subject_identifier)
            
        if 'follow' in schedule_type:

            fu_onschedule_model = child_schedule_dict[cohort]['followup']['onschedule_model']
            fu_schedule_name = child_schedule_dict[cohort]['followup']['name']
            base_appt_datetime = get_utcnow() + relativedelta(months=6)
        
            self.put_on_schedule(onschedule_model=fu_onschedule_model,
                                schedule_name=fu_schedule_name,
                                subject_identifier=self.child_subject_identifier,
                                base_appt_datetime=base_appt_datetime)


            self.delete_completed_appointments(
                appointment_model_cls=ChildAppointment,
                subject_identifier=self.child_subject_identifier,
                schedule_name=schedule_name)

    def put_on_schedule(self, onschedule_model, schedule_name,
                        subject_identifier, base_appt_datetime=None, is_caregiver=False, 
                        onschedule_datetime = get_utcnow()):
        
        

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model,
            name=schedule_name)
        schedule.put_on_schedule(
            subject_identifier=subject_identifier,
            onschedule_datetime=onschedule_datetime,
            base_appt_datetime=base_appt_datetime,
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
                                      schedule_name ):
        """Deletes completed appointments from previous schedules which are present in
        new schedules.

        Args:
            appointment_model_cls (Type[Appointment]): Model class for Appointments.
            subject_identifier (str): Unique identifier for the subject.
            schedule_name (str): New schedule participant is enrolled on.
        Returns:
            None
        """
        complete_appts = appointment_model_cls.objects.filter(
            Q(schedule_name__icontains='quart') | Q(schedule_name__icontains='qt'),
            subject_identifier=subject_identifier, ).exclude(
                appt_status=NEW_APPT).values_list('visit_code', flat=True).distinct()
        
        new_appts = appointment_model_cls.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name=schedule_name,
            visit_code__in=complete_appts)
        if new_appts.exists():
            new_appts.delete()