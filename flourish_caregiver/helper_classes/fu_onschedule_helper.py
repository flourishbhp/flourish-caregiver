from django.apps import apps as django_apps
from django.db.models import Q
from edc_base.utils import get_utcnow
from edc_registration.models import RegisteredSubject

from edc_appointment.constants import NEW_APPT
from edc_appointment.models import Appointment
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from ..models import OnScheduleCohortAFU, OnScheduleCohortBFU
from ..models import OnScheduleCohortBFUQuarterly, OnScheduleCohortCFUQuarterly
from ..models import OnScheduleCohortCFU, OnScheduleCohortAFUQuarterly


class FollowUpEnrolmentHelper(object):
    """Class that puts participant into a followup schedule and reschedules
     consecutive follow ups.

    * Accepts an registered_subject of RegisteredSubject.
    * is called in the dashboard view for subject.

    """

    def __init__(self, subject_identifier, onschedule_datetime=None,
                 update_child=False, cohort=None, schedule_number=None,
                 exception_cls=None):

        self.subject_identifier = subject_identifier
        self.onschedule_datetime = onschedule_datetime or get_utcnow()
        self.update_child = update_child
        self.cohort = cohort
        self.schedule_number = schedule_number

        self.cohort_dict = {'a': OnScheduleCohortAFU,
                            'b': OnScheduleCohortBFU,
                            'c': OnScheduleCohortCFU, }

        self.cohort_quart_dict = {'a': OnScheduleCohortAFUQuarterly,
                                  'b': OnScheduleCohortBFUQuarterly,
                                  'c': OnScheduleCohortCFUQuarterly, }

    def get_latest_completed_appointment(self, subject_identifier, cohort, schedule_number):

        appts = Appointment.objects.filter(~Q(appt_status=NEW_APPT) & ~Q(
            schedule_name__icontains='sec'), subject_identifier=subject_identifier)

        if appts:
            latest = appts.order_by('timepoint').last()
            return latest

    def update_child_identifier_onschedule(self, onschedule_model_cls, subject_identifier,
                                           schedule_name, child_subject_identifier):
        try:
            onschedule_model_cls.objects.get(
                subject_identifier=subject_identifier,
                schedule_name=schedule_name,
                child_subject_identifier=child_subject_identifier)
        except onschedule_model_cls.DoesNotExist:
            try:
                onschedule_obj = onschedule_model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    schedule_name=schedule_name,
                    child_subject_identifier='')
            except onschedule_model_cls.DoesNotExist:
                pass
            else:
                onschedule_obj.child_subject_identifier = (child_subject_identifier)
                onschedule_obj.save()

    def caregiver_off_current_schedule(self, latest_appointment):

        if latest_appointment:

            _, old_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                        name=latest_appointment.schedule_name,
                        onschedule_model=latest_appointment.schedule.onschedule_model)
            old_schedule.take_off_schedule(
                subject_identifier=latest_appointment.subject_identifier)

            return latest_appointment.schedule_name

    def put_on_fu_schedule(self, latest_appt, update_child=False):

        vs = latest_appt.schedule_name.split('_')

        if 'enrol' in latest_appt.schedule_name:
            schedule_name = '_'.join([vs[0], vs[1].replace('enrol', 'fu'), vs[2]])
        elif 'quarterly' in latest_appt.schedule_name:
            schedule_name = '_'.join([vs[0], vs[1].replace('quarterly', 'fu'), vs[2]])
        else:
            schedule_name = '_'.join([vs[0], vs[2].replace('quart', 'fu'), vs[3]])

        onschedule_model_cls = self.cohort_dict.get(schedule_name[0])
        onschedule_quart_model_cls = self.cohort_quart_dict.get(schedule_name[0])

        _, new_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            name=schedule_name,
            onschedule_model=onschedule_model_cls._meta.label_lower)

        new_schedule.put_on_schedule(
            subject_identifier=latest_appt.subject_identifier,
            schedule_name=schedule_name)

        print("Going well..")

        old_onschedule_obj = django_apps.get_model(
                latest_appt.schedule.onschedule_model).objects.get(
                    subject_identifier=latest_appt.subject_identifier,
                    schedule_name=latest_appt.schedule_name)

        self.update_child_identifier_onschedule(
            onschedule_model_cls, latest_appt.subject_identifier, schedule_name,
            old_onschedule_obj.child_subject_identifier)

        self.update_child_identifier_onschedule(
            onschedule_quart_model_cls, latest_appt.subject_identifier, schedule_name,
            old_onschedule_obj.child_subject_identifier)

    def get_related_child_pids(self, subject_identifier):

        related_children = RegisteredSubject.objects.filter(
            subject_identifier__startswith=subject_identifier,
            subject_type='infant')

        return related_children.values_list('subject_identifier', flat=True)

    def activate_fu_schedule(self):

        latest_appt = self.get_latest_completed_appointment(
            self.subject_identifier, self.cohort, self.schedule_number)

        if latest_appt:

            self.put_on_fu_schedule(latest_appt)
            self.caregiver_off_current_schedule(latest_appt)

            print("Done!")
