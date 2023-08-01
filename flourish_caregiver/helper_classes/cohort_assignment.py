from django.apps import apps as django_apps
from edc_base.utils import age

from ..models.caregiver_child_consent import CaregiverChildConsent
from ..models.cohort import Cohort
from ..helper_classes.schedule_dict import child_schedule_dict


class CohortAssignment:

    def __init__(self, child_dob=None, enrolment_dt=None, child_hiv_exposure=None,
                 arv_regimen=None, total_HEU=None, total_HUU=None):
        self.child_dob = child_dob
        self.enrolment_dt = enrolment_dt
        self.child_hiv_exposure = child_hiv_exposure
        self.arv_regimen = arv_regimen
        self.total_HEU = total_HEU
        self.total_HUU = total_HUU

    @property
    def subject_schedule_history_cls(self):
        return django_apps.get_model('edc_visit_schedule.subjectschedulehistory')

    @property
    def child_dataset_cls(self):
        return django_apps.get_model('flourish_child.childdataset')

    def get_study_child_identifier(self, subject_identifier=None):
        consent = CaregiverChildConsent.objects.filter(
            subject_identifier=subject_identifier).first()
        return getattr(consent, 'study_child_identifier', None)

    def child_identifiers(self, cohort):
        """ Return a list of identifiers for child/infant participant's
            onschedule.
            @param cohort: cohort child/infant enrolled for.
            @return: list of enrolled child identifiers.
        """
        identifiers = Cohort.objects.filter(
            name=cohort).values_list('subject_identifier', flat=True)
        study_child_ids = [self.get_study_child_identifier(idx) for idx in identifiers if self.child_onschedule(idx, cohort)]
        return study_child_ids

    def child_onschedule(self, subject_identifier=None, cohort=None):
        """ Checks if infant/child is onschedule by querying their onschedule
            objects.
            @param subject_identifier: child subject_identifier.
        """
        cohort_onschedules = [name_dict.get('name') for name_dict in child_schedule_dict.get(cohort).values()]
        onschedules = self.subject_schedule_history_cls.objects.onschedules(
            subject_identifier=subject_identifier)
        onschedules = [onsch for onsch in onschedules if onsch.schedule_name in cohort_onschedules]
        return bool(onschedules)

    def total_enrolled_HUU(self, cohort):
        """ Return total HIV unexposed uninfected children already enrolled on
            the study.
            @param cohort: cohort child/infant enrolled for
        """
        huu_enrolled = self.child_dataset_cls.objects.filter(
            infant_hiv_exposed__in=['Unexposed', 'unexposed'],
            study_child_identifier__in=self.child_identifiers(cohort))
        return self.total_HUU or huu_enrolled.count()

    def total_enrolled_HEU(self, cohort):
        """ Return total HIV exposed uninfected children already enrolled on
            the study.
        """
        heu_enrolled = self.child_dataset_cls.objects.filter(
            infant_hiv_exposed__in=['Exposed', 'exposed'],
            study_child_identifier__in=self.child_identifiers(cohort))
        return self.total_HEU or heu_enrolled.count()

    @property
    def child_age(self):
        """ Returns infant/child age at enrolment as decimals.
            @return: concat of age and month parsed as decimal.
        """
        child_age = age(self.child_dob, self.enrolment_dt)
        child_age = round(child_age.years + (child_age.months/12) + (child_age.days/365.25), 2)

        return child_age

    @property
    def hiv_exposed_uninfected(self):
        """Return True if child is HEU.
        """
        return self.child_hiv_exposure in ['Exposed', 'exposed']

    @property
    def hiv_unexposed_uninfected(self):
        """Returns True if child is HUU
        """
        return self.child_hiv_exposure in ['Unexposed', 'unexposed']

    @property
    def art_3drug_combination(self):
        return self.arv_regimen == '3-drug ART'

    def cohort_a(self):
        """ Return cohort variable A if the child mother pair meets criteria.
            Criteria:   0 < age <= 5
                        450: total HEU
                        325: total HUU
        """
        cohort = 'cohort_a'
        if self.child_age <= 5:
            if self.hiv_exposed_uninfected and self.total_enrolled_HEU(cohort) < 450:
                return cohort
            elif self.hiv_unexposed_uninfected and self.total_enrolled_HUU(cohort) < 325:
                return cohort
            return 'cohort_a_sec'

    def cohort_b(self):
        """ Return cohort variable B if child mother pair meets criteria.
            Criteria:   5 < age <= 10
                        ART regimen: 3-drug ART for HEU
                        200: total HEU
                        100: total HUU
        """
        cohort = 'cohort_b'
        if self.child_age > 5 and self.child_age <= 10:
            if (self.hiv_exposed_uninfected and
                    self.art_3drug_combination and self.total_enrolled_HEU(cohort) < 200):
                return cohort
            elif self.hiv_unexposed_uninfected and self.total_enrolled_HUU(cohort) < 100:
                return cohort
            return 'cohort_b_sec'

    def cohort_c(self):
        """ Return cohort variable C if child mother pair meets criteria.
            Criteria:   age > 10
                        ART regimen: 3-drug ART for HEU
                        100: total HEU
                        200: total HUU
        """
        cohort = 'cohort_c'
        if self.child_age > 10:
            if (self.hiv_exposed_uninfected and
                    self.art_3drug_combination and self.total_enrolled_HEU(cohort) < 100):
                return cohort
            elif self.hiv_unexposed_uninfected and self.total_enrolled_HUU(cohort) < 200:
                return cohort
            return 'cohort_c_sec'

    @property
    def cohort_variable(self):
        return self.cohort_a() or self.cohort_b() or self.cohort_c()
