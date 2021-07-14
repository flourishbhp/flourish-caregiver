import re
from django.apps import apps as django_apps
from edc_base.utils import age
from flourish_child.models import ChildDataset
from ..models.subject_consent import SubjectConsent
from ..models.maternal_dataset import MaternalDataset


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
        self._screening_identifiers = SubjectConsent.objects.values_list(
            'screening_identifier', flat=True).distinct()

    def age_at_enrollment(self, child_dob=None, check_date=None):
        """Returns age months as decimals.
        """
        child_dob = child_dob or self.child_dob
        check_date = check_date or self.enrollment_date

        child_age = age(child_dob, check_date)

        child_age = str(child_age.years) + '.' + str(child_age.months)
        print(child_age)
        return float(re.search(r'\d+.\d+', child_age).group())

    @property
    def hiv_exposed_uninfected(self):
        """Return True is an infant is HEU.
        """
        return self.infant_hiv_exposed == 'Exposed'

    @property
    def hiv_unexposed_uninfected(self):
        """Returns True if an infant is HUU
        """
        return self.infant_hiv_exposed == 'Unexposed'

    @property
    def huu_adolescents(self):
        """Returns True if the infant is HUU and is an Adolescent.
        """
        return self.age_at_enrollment() >= 10 and self.hiv_unexposed_uninfected

    @property
    def no_hiv_during_preg(self):
        """Return True if the infant had no explore to HIV during pregnancy.
        """
        return self.mum_hiv_status == 'HIV uninfected'

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

    @property
    def total_efv_regime(self):
        """Return total enrolled infant for a specified protocol with EFV regime.
        """

        maternal_dataset = MaternalDataset.objects.filter(
            screening_identifier__in=self._screening_identifiers,
            preg_efv=1)
        return maternal_dataset.count()

    @property
    def total_dtg_regime(self):
        """Return total enrolled infant for a specified protocol with DTG regime.
        """
        maternal_dataset = MaternalDataset.objects.filter(
            screening_identifier__in=self._screening_identifiers,
            preg_dtg=1)
        return maternal_dataset.count()

    @property
    def total_pi_regime(self):
        """Returns total enrolled infants for a specified protocol with PI regime.
        """
        maternal_dataset = MaternalDataset.objects.filter(
            screening_identifier__in=self._screening_identifiers,
            preg_pi=1)
        return maternal_dataset.count()

    def total_HEU(self, protocol=None):
        """Return total enrolled Tshilo Dikotla HEU.
        """

        study_maternal_identifiers = MaternalDataset.objects.values_list(
            'study_maternal_identifier', flat=True).filter(
                screening_identifier__in=self._screening_identifiers)

        child_dataset = ChildDataset.objects.filter(
            study_maternal_identifier__in=study_maternal_identifiers,
            infant_hiv_exposed='Exposed')
        return child_dataset.count()

    @property
    def total_no_hiv_during_preg(self):
        """Return total number of infants with no HIV expore.
        """
        maternal_dataset = MaternalDataset.objects.filter(
            screening_identifier__in=self._screening_identifiers,
            mom_hivstatus='HIV uninfected')
        return maternal_dataset.count()

    def total_HUU(self, protocol=None):
        """Returns total enrolled Tshilo Dikotla HUU infants.
        """

        caregiver_child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

        child_offstudy_cls = django_apps.get_model(
            'flourish_prn.childoffstudy')

        study_maternal_identifiers = MaternalDataset.objects.values_list(
            'study_maternal_identifier', flat=True).filter(
            protocol=protocol)

        study_child_identifiers = ChildDataset.objects.filter(
            study_maternal_identifier__in=study_maternal_identifiers,
            infant_hiv_exposed='Unexposed').values_list(
            'study_child_identifier', flat=True)

        child_offstudies = child_offstudy_cls.objects.all().values_list(
            'subject_identifier', flat=True)

        child_subject_identifiers = caregiver_child_consent_cls.objects.values_list(
            'subject_identifier', flat=True).filter(
                child_age_at_enrollment__lte=2.5,
                study_child_identifier=study_child_identifiers)

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
            infant_hiv_exposed='Unexposed')
        return child_dataset.count()

    @property
    def age_at_year_3(self):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3
        return self.age_at_enrollment(child_dob=self.child_dob, check_date=start_date_year_3)

    def cohort_a(self):
        """Return True if the infant mother pair meets criteria for cohort A.
        """
        # TODO: Cater for 200 newly enrolled pregnant woman.
        if self.age_at_enrollment() <= 2.5 and self.age_at_year_3 <= 4.5:
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
        if (self.age_at_enrollment() >= 4 and self.age_at_enrollment() <= 8.5
                and self.age_at_year_3 >= 6 and self.age_at_year_3 <= 10.5):

            if self.protocol in protocols and self.efv_regime:
                return 'cohort_b' if self.total_efv_regime < 100 else 'cohort_b_sec'

            elif self.protocol in protocols and self.dtg_regime:
                return 'cohort_b' if self.total_dtg_regime < 100 else 'cohort_b_sec'

            elif self.protocol in protocols and self.no_hiv_during_preg:
                return 'cohort_b' if self.total_no_hiv_during_preg < 100 else 'cohort_b_sec'

            return 'cohort_b_sec'

    def cohort_c(self):
        """Return True id an infant mother pair meets criteria for cohort C.
        """
        # TODO: cater for 125 new enrolled adolescents
        if (self.age_at_enrollment() >= 8 and self.age_at_enrollment() <= 17.9
                and self.age_at_year_3 >= 10):
            if self.huu_adolescents:
                return ('cohort_c' if self.protocol == 'Tshipidi'
                        and self.total_huu_adolescents(protocol='Tshipidi') < 75
                        else 'cohort_c_sec')
                return True
            elif self.pi_regime:
                return ('cohort_c' if self.protocol in ['Mma Bana', 'Mpepu', 'Tshipidi']
                        and self.total_pi_regime < 100 else 'cohort_c_sec')
            return 'cohort_c_sec'

    @property
    def cohort_variable(self):
        return self.cohort_a() or self.cohort_b() or self.cohort_c()
