from django.apps import apps as django_apps
from edc_base.utils import age

from flourish_child.models import ChildDataset

from ..models.maternal_dataset import MaternalDataset
from ..models.subject_consent import SubjectConsent


class CohortError(Exception):
    pass


class Cohort:

    """Class that determines the cohort that a child belong to
    """

    def __init__(
            self, child_dob=None, enrollment_date=None, infant_hiv_exposed=None,
            mum_hiv_status=None, protocol=None, dtg=None, pi=None, efv=None,
            screening_identifier=None):

        self.child_dob = child_dob
        self.enrollment_date = enrollment_date
        self.infant_hiv_exposed = infant_hiv_exposed
        self.mum_hiv_status = mum_hiv_status
        self.protocol = protocol
        self.dtg = dtg
        self.pi = pi
        self.efv = efv
        self.caregiver_child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')
        self._screening_identifiers = SubjectConsent.objects.values_list(
            'screening_identifier', flat=True).distinct()
        app_config = django_apps.get_app_config('flourish_caregiver')
        self.start_date_year_3 = app_config.start_date_year_3

    def age_at_enrollment(self, child_dob=None, check_date=None):
        """Returns age months as decimals.
        """
        child_dob = child_dob or self.child_dob
        check_date = check_date or self.enrollment_date

        if check_date > child_dob:
            child_age = age(child_dob, check_date)
            child_age = str(child_age.years) + '.' + str(child_age.months)
        else:
            child_age = 0
        return float(child_age)

    @property
    def hiv_exposed_uninfected(self):
        """Return True is an infant is HEU.
        """
        return self.infant_hiv_exposed in ['Exposed', 'exposed']

    @property
    def hiv_unexposed_uninfected(self):
        """Returns True if an infant is HUU
        """
        return self.infant_hiv_exposed in ['Unexposed', 'unexposed']

    @property
    def huu_adolescents(self):
        """Returns True if the infant is HUU and is an Adolescent.
        """
        return self.age_at_enrollment() >= 10 and self.hiv_unexposed_uninfected

    @property
    def no_hiv_during_preg(self):
        """Return True if the infant had no explore to HIV during pregnancy.
        """
        return self.mum_hiv_status == 'HIV-uninfected'

    @property
    def efv_regime(self):
        """."""
        return self.efv == 1

    @property
    def dtg_regime(self):
        """Returns True if the mother used dtg during pregnancy.
        """
        return self.dtg == 1

    @property
    def pi_regime(self):
        """Returns True if the mother used pi during pregnancy.
        """
        return self.pi == 1

    def total_efv_regime(self, cohort=None):
        """Return total enrolled infant for a specified protocol with EFV regime.
        """

        maternal_dataset_ids = MaternalDataset.objects.filter(
            preg_efv=1).values_list('screening_identifier', flat=True)

        efv_consents = SubjectConsent.objects.filter(
            screening_identifier__in=maternal_dataset_ids)

        efv_consented = self.caregiver_child_consent_cls.objects.filter(
            subject_consent__in=efv_consents,
            cohort=cohort)

        return efv_consented.count()

    def total_dtg_regime(self, cohort=None):
        """Return total enrolled infant for a specified protocol with DTG regime.
        """
        maternal_dataset_ids = MaternalDataset.objects.filter(
            preg_dtg=1).values_list('screening_identifier', flat=True)

        dtg_consents = SubjectConsent.objects.filter(
            screening_identifier__in=maternal_dataset_ids)

        dtg_consented = self.caregiver_child_consent_cls.objects.filter(
            subject_consent__in=dtg_consents,
            cohort=cohort)

        return dtg_consented.count()

    def total_pi_regime(self, cohort=None):
        """Returns total enrolled infants for a specified protocol with PI regime.
        """
        maternal_dataset_ids = MaternalDataset.objects.filter(
            preg_pi=1).values_list('screening_identifier', flat=True)

        pi_consents = SubjectConsent.objects.filter(
            screening_identifier__in=maternal_dataset_ids)

        pi_consented = self.caregiver_child_consent_cls.objects.filter(
            subject_consent__in=pi_consents,
            cohort=cohort)

        return pi_consented.count()

    def total_HEU(self, protocol=None):
        """Return total enrolled Tshilo Dikotla HEU.
        """

        study_maternal_identifiers = MaternalDataset.objects.values_list(
            'study_maternal_identifier', flat=True).filter(
                screening_identifier__in=self._screening_identifiers,
                protocol=protocol)

        child_dataset = ChildDataset.objects.filter(
            study_maternal_identifier__in=study_maternal_identifiers,
            infant_hiv_exposed='Exposed')
        return child_dataset.count()

    def total_no_hiv_during_preg(self, cohort=None):
        """Return total number of infants with no HIV expore.
        """
        maternal_dataset_ids = MaternalDataset.objects.filter(
            mom_hivstatus='HIV-uninfected')

        no_hiv_consents = SubjectConsent.objects.filter(
            screening_identifier__in=maternal_dataset_ids)

        no_hiv_consented = self.caregiver_child_consent_cls.objects.filter(
            subject_consent__in=no_hiv_consents,
            cohort=cohort)

        return no_hiv_consented.count()

    def total_HUU(self, protocol=None):
        """Returns total enrolled Tshilo Dikotla HUU infants.
        """

        child_offstudy_cls = django_apps.get_model(
            'flourish_prn.childoffstudy')

        study_maternal_identifiers = MaternalDataset.objects.values_list(
            'study_maternal_identifier', flat=True).filter(
            protocol=protocol)

        study_child_identifiers = ChildDataset.objects.filter(
            study_maternal_identifier__in=study_maternal_identifiers,
            infant_hiv_exposed__in=['Unexposed', 'unexposed']).values_list(
            'study_child_identifier', flat=True)

        child_offstudies = child_offstudy_cls.objects.all().values_list(
            'subject_identifier', flat=True)

        child_subject_identifiers = self.caregiver_child_consent_cls.objects.filter(
                child_age_at_enrollment__lte=2.5,
                study_child_identifier__in=study_child_identifiers).values_list(
            'subject_identifier', flat=True)

        onstudy_huu = list(set(child_subject_identifiers) - set(child_offstudies))

        return len(onstudy_huu)

    def total_huu_adolescents(self, protocol=None):
        """Return total enrolled infant that are HUU adolescents.
        Total returned is for a protocol specified.
        """

        caregiver_child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

        screening_identifiers = caregiver_child_consent_cls.objects.values_list(
            'subject_consent__screening_identifier', flat=True).filter(
                child_age_at_enrollment__gte=9.5)

        study_maternal_identifiers = MaternalDataset.objects.values_list(
            'study_maternal_identifier', flat=True).filter(
                screening_identifier__in=screening_identifiers)

        child_dataset = ChildDataset.objects.filter(
            study_maternal_identifier__in=study_maternal_identifiers,
            infant_hiv_exposed__in=['Unexposed', 'unexposed'])
        return child_dataset.count()

    @property
    def age_at_year_3(self):
        """Returns the age at year 3.
        """
        return self.age_at_enrollment(child_dob=self.child_dob,
                                      check_date=self.start_date_year_3)

    @property
    def year3_benchmark(self):

        age_mark = False
        if self.start_date_year_3 > self.enrollment_date:
            age_mark = True

        return age_mark

    @property
    def check_age(self):

        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        if self.enrollment_date > start_date_year_3:
            check_age = self.age_at_enrollment()
        else:
            check_age = self.age_at_year_3

        return check_age

    def cohort_a(self):
        """Return True if the infant mother pair meets criteria for cohort A.
        """
        # TODO: Cater for 200 newly enrolled pregnant woman.

        if self.check_age <= 5:
            if (self.protocol == 'Tshilo Dikotla' and self.hiv_exposed_uninfected
                    and self.total_HEU(protocol='Tshilo Dikotla') < 200):
                return 'cohort_a'
            elif(self.protocol == 'Tshilo Dikotla' and self.hiv_unexposed_uninfected
                    and self.total_HUU(protocol='Tshilo Dikotla') < 75):
                return 'cohort_a'
            return 'cohort_a_sec'

    def cohort_b(self):
        """Return True id an infant mother pair meets criteria for cohort B.
        """
        protocols = ['Tshilo Dikotla', 'Mpepu', 'Tshipidi']

        if self.check_age > 5 and self.check_age <= 10.5:

            if self.protocol in protocols and self.efv_regime:
                return ('cohort_b' if self.total_efv_regime(
                    cohort='cohort_b') < 100 else 'cohort_b_sec')

            elif self.protocol in protocols and self.dtg_regime:
                return ('cohort_b' if self.total_dtg_regime(
                    cohort='cohort_b') < 100 else 'cohort_b_sec')

            elif self.protocol in protocols and self.no_hiv_during_preg:
                return ('cohort_b' if self.total_no_hiv_during_preg(
                    cohort='cohort_b') < 100 else 'cohort_b_sec')

            return 'cohort_b_sec'

    def cohort_c(self):
        """Return True id an infant mother pair meets criteria for cohort C.
        """
        # TODO: cater for 125 new enrolled adolescents
        if self.check_age >= 10:
            if self.huu_adolescents:
                return ('cohort_c' if self.protocol == 'Tshipidi'
                        and self.total_huu_adolescents(protocol='Tshipidi') < 75
                        else 'cohort_c_sec')
                return True
            elif self.pi_regime:
                return ('cohort_c' if self.protocol in ['Mma Bana', 'Mpepu', 'Tshipidi']
                        and self.total_pi_regime(cohort='cohort_c') < 100 else 'cohort_c_sec')
            return 'cohort_c_sec'

    @property
    def cohort_variable(self):
        return self.cohort_a() or self.cohort_b() or self.cohort_c()
