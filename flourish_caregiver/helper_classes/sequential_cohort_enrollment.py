from django.apps import apps as django_apps
from edc_base.utils import get_utcnow, age
from .cohort_assignment import CohortAssignment
from ..models import MaternalDataset
from .seq_enrol_onschedule_mixin import SeqEnrolOnScheduleMixin
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
    def cohort_cls(self):
        return django_apps.get_model(self.cohort_model)

    def cohort_assigned(self, study_child_identifier, child_dob, enrollment_date):
        """Calculates participant's cohort based on the maternal and child dataset
        """
        infant_dataset_obj = None
        try:
            infant_dataset_obj = self.infant_dataset_cls.objects.get(
                study_child_identifier=study_child_identifier,
                dob=child_dob)
        except self.infant_dataset_cls.DoesNotExist:
            pass
        except self.infant_dataset_cls.MultipleObjectsReturned:
            infant_dataset_obj = self.infant_dataset_cls.objects.filter(
                study_child_identifier=study_child_identifier,
                dob=child_dob)[0]
        finally:
            try:
                maternal_dataset_obj = MaternalDataset.objects.get(
                    study_maternal_identifier=getattr(
                        infant_dataset_obj, 'study_maternal_identifier', None))
            except MaternalDataset.DoesNotExist:
                return None
            else:
                cohort = CohortAssignment(
                    child_dob=child_dob,
                    enrolment_dt=enrollment_date,
                    child_hiv_exposure=getattr(
                        infant_dataset_obj, 'infant_hiv_exposed', None),
                    arv_regimen=getattr(
                        maternal_dataset_obj, 'mom_pregarv_strat', None), )
                return cohort.cohort_variable or None

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
    def schedule_name(self):
        return self.cohort_obj.schedule_name

    @property
    def onschedule_model(self):
        return self.cohort_obj.onschedule_model

    @property
    def schedule_type(self):
        return self.cohort_obj.name

    @property
    def current_quartarly_schedule_type(self):
        return self.cohort_obj.name if 'quart' in self.cohort_obj.name else None

    @property
    def evaluated_cohort(self):
        """Return cohort name evaluated now.
        """
        return self.cohort_assigned(
            child_dob=self.child_consent_obj.child_dob,
            study_child_identifier=self.child_consent_obj.study_child_identifier,
            enrollment_date=get_utcnow().date(),
        )
