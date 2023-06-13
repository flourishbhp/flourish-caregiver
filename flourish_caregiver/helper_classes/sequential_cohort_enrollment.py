from django.apps import apps as django_apps
from django.db.models import Q
from edc_base.utils import get_utcnow, age
from .cohort_assignment import CohortAssignment
from ..models import MaternalDataset
from .sequential_onschedule_mixin import SeqEnrolOnScheduleMixin
from .sequential_offschedule_mixin import OffScheduleSequentialCohortEnrollmentMixin
from ..models.signals import cohort_assigned


class SequentialCohortEnrollmentError(Exception):
    pass


class SequentialCohortEnrollment(SeqEnrolOnScheduleMixin,
                                 OffScheduleSequentialCohortEnrollmentMixin):
    """Class that checks and enrols participants to the next
    the next cohort when they age up.
    """

    subject_schedule_model = 'edc_visit_schedule.subjectschedulehistory'

    child_consent_model = 'flourish_caregiver.caregiverchildconsent'

    infant_dataset_model = 'flourish_child.childdataset'

    cohort_model = 'flourish_caregiver.cohort'

    def __init__(self, child_subject_identifier=None):
        self.child_subject_identifier = child_subject_identifier
        self.cohort_assignment = CohortAssignment(
            child_dob=self.child_dob,
            enrolment_dt=get_utcnow())

    @property
    def child_consent_cls(self):
        return django_apps.get_model(self.child_consent_model)

    @property
    def infant_dataset_cls(self):
        return django_apps.get_model(self.infant_dataset_model)

    @property
    def subject_schedule_cls(self):
        return django_apps.get_model(self.subject_schedule_model)

    @property
    def subject_schedule_cls(self):
        return django_apps.get_model(self.subject_schedule_model)

    @property
    def child_last_qt_subject_schedule_obj(self):
        try:
            schedule_obj = self.subject_schedule_cls.objects.filter(
                Q(schedule_name__icontains='qt') | Q(
                    schedule_name__icontains='quart'),
                subject_identifier=self.child_consent_obj.subject_identifier,

            ).latest('onschedule_datetime')
        except self.subject_schedule_cls.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f'{self.child_consent_obj.subject_identifier} : was never been on quartarly schedule')
        else:
            return schedule_obj

    @property
    def cohort_obj(self):
        try:
            cohort_obj = self.cohort_cls.objects.filter(
                subject_identifier=self.child_subject_identifier).latest('assign_datetime')
        except self.cohort_cls.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f'{self.child_subject_identifier} : cohort instance does not exist')
        else:
            return cohort_obj

    @property
    def caregiver_subject_identifier(self):
        """Return child caregiver subject identifier.
        """
        return self.child_consent_obj.subject_consent.subject_identifier

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
    def child_count(self):
        return self.child_consent_obj.caregiver_visit_count

    @property
    def child_dob(self):
        return self.child_consent_obj.child_dob

    @property
    def schedule_type(self):

        schedule_name = self.child_last_qt_subject_schedule_obj.schedule_name

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
        return cohort_assigned(
            child_dob=self.child_consent_obj.child_dob,
            study_child_identifier=self.child_consent_obj.study_child_identifier,
            enrollment_date=get_utcnow().date(),
        )

    def put_onschedule(self):
        self.take_off_child_offschedule()
        self.take_off_caregiver_offschedule()
        self.put_child_onschedule()
        self.put_caregiver_onschedule()
