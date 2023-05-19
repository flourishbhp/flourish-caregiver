from django.apps import apps as django_apps
from edc_constants.date_constants import timezone

from .cohort import Cohort
from ..models import (
    AntenatalEnrollment, CaregiverPreviouslyEnrolled,
    CaregiverChildConsent)


class SequentialCohortEnrollmentError(Exception):
    pass


class SequentialCohortEnrollment:

    """Class that checks and enrols participants to the next
    the next cohort when they age up.
    """

    def __init__(self, child_subject_identifier=None):
        
        self.child_subject_identifier = child_subject_identifier
    
    @property
    def caregiver_subject_identifier(self):
        """Return child caregiver subject identifier.
        """
        registration_mdl_cls = django_apps.get_model('edc_registration', 'registeredsubject')
        try:
            registered_subject = registration_mdl_cls.objects.get(
                subject_identifier=self.child_subject_identifier)
        except registration_mdl_cls.DoesNotExist:
            return None
        else:
            registered_subject.relative_identifier
        return None


    def check_enrollment(self):
        """Return True if the child is enrolled.
        """
        enrolled = False
        try:
            AntenatalEnrollment.objects.get(
                subject_identifier=self.caregiver_subject_identifier)
        except AntenatalEnrollment.DoesNotExist:
            enrolled = False
        else:
            enrolled = True

        try:
            CaregiverPreviouslyEnrolled.objects.get(
                subject_idetifier=self.caregiver_subject_identifier)
        except CaregiverPreviouslyEnrolled.DoesNotExist:
            enrolled = False
        else:
            enrolled = True
        return enrolled
    
    @property
    def enrollment_cohort(self):
        """Returns the cohort the child was enrolled on the first time.
        """
        cohort = None
        try:
            cohort =  Cohort.objects.get(
                subject_identifier=self.child_subject_identifier)
        except Cohort.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f"The subject: {self.child_subject_identifier} does not "
                "have an enrollment cohort")
        else:
            cohort = cohort.name
        return cohort

    @property
    def child_current_age(self):
        try:
            caregiver_child_consent =  CaregiverChildConsent.objects.get(
                study_child_identifier=self.child_subject_identifier)
        except CaregiverChildConsent.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f"The subject: {self.child_subject_identifier} does not "
                "have a caregiver child consent")
        else:
            dob = caregiver_child_consent.child_dob
            age = Cohort(
                child_dob=dob,
                enrollment_date=timezone.now().date())
            return age
        return None

    @property
    def aged_up(self):
        """Return true if the child has aged up on the cohort
        they are currently enrolled on
        """
        if self.current_cohort == 'cohort_a':
            if self.child_current_age >= 5:
                return True
        elif self.current_cohort == 'cohort_b':
            if self.child_current_age > 10:
                True
        return False
    
    @property
    def current_cohort(self):
        """Returns the cohort the child was enrolled on the first time.
        """
        cohort = Cohort.objects.objects(
            suject_identifier=self.child_subject_identifier).order_by(
                'assign_datetime'
            )
        if cohort:
            return cohort.name
        return None

    @property
    def enroll_on_age_up_cohort(self):
        """Enroll a participant on new aged up cohort.
        """
        pass

    @property
    def take_off_schedule(self):
        """Take participant off schedule from previous age cohort.
        """
        pass