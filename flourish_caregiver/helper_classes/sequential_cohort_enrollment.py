from django.apps import apps as django_apps
from edc_base.utils import get_utcnow, age
from .cohort_assignment import CohortAssignment


class SequentialCohortEnrollmentError(Exception):
    pass


class OffScheduleSequentialCohortEnrollmentMixin:
    def put_caregiver_offschedule(self):
        pass

    def put_child_offschedule(self):
        pass


class OnScheduleSequentialCohortEnrollmentMixin:
    def put_caregiver_onschedule(self):
        pass

    def put_child_onschedule(self):
        pass


class SequentialCohortEnrollment(OnScheduleSequentialCohortEnrollmentMixin,
                                 OffScheduleSequentialCohortEnrollmentMixin):
    """Class that checks and enrols participants to the next
    the next cohort when they age up.
    """

    subject_schedule_model = 'edc_visit_schedule.subjectschedulehistory'

    child_consent_model = 'flourish_caregiver.caregiverchildconsent'

    def __init__(self, child_subject_identifier=None):
        self.child_subject_identifier = child_subject_identifier
        self.cohort_assignment = CohortAssignment(
            child_dob=self.child_dob,
            enrolment_dt=get_utcnow())

    @property
    def child_consent_cls(self):
        return django_apps.get_model(self.child_consent_model)

    @property
    def subject_schedule_cls(self):
        return django_apps.get_model(self.subject_schedule_model)

    @property
    def latest_quartarly_schedule(self):
        """Returns latest quartly call only

        Returns:
            subject_schedule_cls | None: returns latest quartarly call or None if the child is not
            any quarterly schedule
        """
        try:
            schedule_history = self.subject_schedule_cls.objects.filter(
                subject_identifier=self.subject_identifier,
                schedule_name__icontains='quart'
            ).only('onschedule_datetime', 'schedule_name').latest('onschedule_datetime')

        except self.subject_schedule_cls.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f"The subject: {self.child_subject_identifier} was not enrolled")
        else:
            return schedule_history

    @property
    def caregiver_subject_identifier(self):
        """Return child caregiver subject identifier.
        """
        return self.child_subject_identifier[:-3]

    @property
    def child_consent_obj(self):
        try:
            consent_obj = self.child_consent_cls.objects.filter(
                subject_identifier=self.child_subject_identifier
            ).only('child_dob', 'caregiver_visit_count').latest('version')
        except self.child_consent_cls.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f"The subject: {self.child_subject_identifier} does not "
                "have a caregiver child consent")
        else:
            return consent_obj

    @property
    def child_current_age(self):
        return age(self.child_dob, get_utcnow()).years

    @property
    def child_dob(self):
        return self.child_consent_obj.child_dob

    @property
    def current_cohort(self):
        """Returns the cohort the child was enrolled on the first time.
        """
        schedule_name = self.latest_quartarly_schedule.schedule_name

        cohort_name = f"cohort_{schedule_name[0]}"

        if 'sec' in schedule_name:
            cohort_name += '_sec'

        return cohort_name

    @property
    def current_schedule_type(self):
        schedule_name = self.latest_quartarly_schedule.schedule_name

        if 'fu' in schedule_name:
            return 'followup_quartaly'
        elif 'sec' in schedule_name:
            return 'sec_aims_quart'
        else:
            return 'quarterly'

    @property
    def evaluated_cohort(self):
        """Return cohort name evaluated now.
        """
        return self.cohort_assignment.cohort_variable

    def put_caregiver_and_child_onschedule(self):
        self.put_child_onschedule()
        self.put_caregiver_onschedule()

    def put_caregiver_and_child_offschedule(self):
        self.put_child_offschedule()
        self.put_caregiver_offschedule()
