from django.apps import apps as django_apps
from django.db.models import Q
from edc_base.utils import age, get_utcnow

from .utils import cohort_assigned
from ..models.cohort import Cohort
from .sequential_onschedule_mixin import SeqEnrolOnScheduleMixin
from .sequential_offschedule_mixin import OffScheduleSequentialCohortEnrollmentMixin


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
    def child_last_qt_subject_schedule_obj(self):
        try:
            schedule_obj = self.subject_schedule_cls.objects.filter(
                Q(schedule_name__icontains='qt') | Q(
                    schedule_name__icontains='quart'),
                subject_identifier=self.child_consent_obj.subject_identifier,

            ).latest('onschedule_datetime')
        except self.subject_schedule_cls.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f'{self.child_consent_obj.subject_identifier} : was never been on '
                f'quartarly schedule')
        else:
            return schedule_obj

    @property
    def caregiver_last_qt_subject_schedule_obj(self):
        try:
            schedule_obj = self.subject_schedule_cls.objects.filter(
                Q(schedule_name__icontains='qt') | Q(
                    schedule_name__icontains='quart'),
                subject_identifier=self.caregiver_subject_identifier,

            ).latest('onschedule_datetime')
        except self.subject_schedule_cls.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f'{self.caregiver_subject_identifier} : was never been on quartarly '
                f'schedule')
        else:
            return schedule_obj

    @property
    def cohort_obj(self):
        try:
            cohort_obj = self.cohort_cls.objects.filter(
                subject_identifier=self.child_subject_identifier).latest(
                'assign_datetime')
        except self.cohort_cls.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f'{self.child_subject_identifier} : cohort instance does not exist')
        else:
            return cohort_obj

    @property
    def caregiver_subject_identifier(self):
        """Return child caregiver subject identifier.
        """
        return self.caregiver_consent_obj.subject_identifier

    @property
    def caregiver_consent_obj(self):
        return self.child_consent_obj.subject_consent

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
            return 'followup_quarterly'
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

        if 'followup_quarterly' == self.schedule_type and\
            'sec' in self.evaluated_cohort:
            return

        self.take_off_child_offschedule()
        self.take_off_caregiver_offschedule()
        self.put_child_onschedule()
        self.put_caregiver_onschedule()

    @property
    def child_current_age(self):
        """Returns age months as decimals.
        """
        check_date = get_utcnow().date()
        caregiver_child_consent = self.child_consent_cls.objects.filter(
            subject_identifier=self.child_subject_identifier).last()
        dob = caregiver_child_consent.child_dob
        if dob:
            if check_date > dob:
                child_age = age(dob, check_date)
                child_age = str(child_age.years) + '.' + str(child_age.months)
            else:
                child_age = 0
            return float(child_age)
        return None

    @property
    def current_cohort(self):
        """Returns the cohort the child was enrolled on the first time.
        """

        cohort = Cohort.objects.filter(
            subject_identifier=self.child_subject_identifier).order_by(
            'assign_datetime').last()
        if cohort:
            return cohort.name
        return None

    @property
    def aged_up(self):
        """Return true if the child has aged up on the cohort
        they are currently enrolled on
        """
        if self.child_current_age:
            if self.current_cohort in ['cohort_a', 'cohort_a_sec']:
                if self.child_current_age >= 5:
                    return True
            elif self.current_cohort in ['cohort_b', 'cohort_b_sec']:
                if self.child_current_age > 10:
                    return True
        return False

    def age_up_enrollment(self):
        """Checks if a child has aged up and put the on a new cohort and schedule.
        """
        # Check if a child has aged up
        if self.aged_up and self.current_cohort != self.evaluated_cohort:
            # put them on a new aged up cohort

            defaults = {
                'assign_datetime': get_utcnow(),
                'enrollment_cohort': False
            }
            cohort_obj, _ = Cohort.objects.get_or_create(
                defaults=defaults, subject_identifier=self.child_subject_identifier,
                name=self.evaluated_cohort, )
            # Put caregiver and child off and on schedule
            if cohort_obj:
                self.put_onschedule()
