import re
from django.apps import apps as django_apps

from flourish_child.models import ChildDataset

from ..models import SubjectConsent, MaternalDataset


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

    def age_at_enrollment(self, child_dob=None, check_date=None):
        """Returns age months as decimals.
        """
        child_dob = child_dob or self.child_dob
        check_date = check_date or self.enrollment_date

        current_date = check_date
        current_month = check_date.month
        current_year = check_date.year
        birth_date = child_dob
        birth_month = child_dob.month
        birth_year = child_dob.year

        month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (birth_date > current_date):
            current_month = current_month - 1
            current_date = current_date + month[birth_month - 1]


        # if birth month exceeds current month, then
        # donot count this year and add 12 to the
        # month so that we can subtract and find out
        # the difference
        if (birth_month > current_month):
            current_year = current_year - 1;
            current_month = current_month + 12;

        # calculate date, month, year
        calculated_month = current_month - birth_month;
        calculated_year = current_year - birth_year;

        age = str(calculated_year) + '.' + str(calculated_month)
        return float(re.search(r'\d+.\d+', age).group())

    @property
    def hiv_exposed_uninfected(self,):
        """Return True is an infant is HEU.
        """
        if self.infant_hiv_exposed == 'Exposed':
            return True
        return False

    @property
    def hiv_unexposed_uninfected(self):
        """Returns True if an infant is HUU
        """
        if self.infant_hiv_exposed == 'Unexposed':
            return True
        return False

    @property
    def huu_adolescents(self):
        """Returns True if the infant is HUU and is an Adolescent.
        """
        if self.age_at_enrollment() >= 10 and self.hiv_unexposed_uninfected:
            return True
        return False

    @property
    def no_hiv_during_preg(self):
        """Return True if the infant had no explore to HIV during pregnancy.
        """
        if self.mum_hiv_status == 'HIV uninfected':
            return True
        return False

    @property
    def efv_regime(self):
        """."""
        if self.efv == 1:
            return True
        return False

    @property
    def dtg_regime(self):
        """Returns True if the mother used dtg during pregnancy.
        """
        if self.dtg == 1:
            return True
        return False

    @property
    def pi_regime(self):
        """Returns True if the mother used pi during pregnancy.
        """
        if self.pi == 1:
            return True
        return False

    @property
    def total_efv_regime(self):
        """Return total enrolled infant for a specified protocol with EFV regime.
        """
        screening_identifiers = SubjectConsent.objects.values_list(
            'screening_identifier', flat=True).distinct()
        maternal_dataset = MaternalDataset.objects.filter(
            screening_identifier__in=screening_identifiers,
            preg_efv=1)
        return maternal_dataset.count()

    @property
    def total_dtg_regime(self):
        """Return total enrolled infant for a specified protocol with DTG regime.
        """
        screening_identifiers = SubjectConsent.objects.values_list(
            'screening_identifier', flat=True).distinct()
        maternal_dataset = MaternalDataset.objects.filter(
            screening_identifier__in=screening_identifiers,
            preg_dtg=1)
        return maternal_dataset.count()

    @property
    def total_pi_regime(self):
        """Returns total enrolled infants for a specified protocol with PI regime.
        """
        screening_identifiers = SubjectConsent.objects.values_list(
            'screening_identifier', flat=True).distinct()
        maternal_dataset = MaternalDataset.objects.filter(
            screening_identifier__in=screening_identifiers,
            preg_pi=1)
        return maternal_dataset.count()

    def total_HEU(self, protocol=None):
        """Return total enrolled Tshilo Dikotla HEU.
        """
        screening_identifiers = SubjectConsent.objects.values_list(
            'screening_identifier', flat=True).distinct()
        
        study_child_identifiers = MaternalDataset.objects.values_list(
            'study_child_identifier', flat=True).filter(
                screening_identifier__in=screening_identifiers)
        
        child_dataset = ChildDataset.objects.filter(
            study_child_identifiers__in=study_child_identifiers,
            infant_hiv_exposed='Exposed')
        return child_dataset.count()

    @property
    def total_no_hiv_during_preg(self):
        """Return total number of infants with no HIV expore.
        """
        screening_identifiers = SubjectConsent.objects.values_list(
            'screening_identifier', flat=True).distinct()
        maternal_dataset = MaternalDataset.objects.filter(
            screening_identifier__in=screening_identifiers,
            mum_hiv_status='HIV uninfected')
        return maternal_dataset.count()
        

    def total_HUU(self, protocol=None):
        """Returns total enrolled Tshilo Dikotla HUU infants.
        """
        screening_identifiers = SubjectConsent.objects.values_list(
            'screening_identifier', flat=True).distinct()
        
        study_child_identifiers = MaternalDataset.objects.values_list(
            'study_child_identifier', flat=True).filter(
                screening_identifier__in=screening_identifiers)
        
        child_dataset = ChildDataset.objects.filter(
            study_child_identifiers__in=study_child_identifiers,
            infant_hiv_exposed='Unexposed')
        return child_dataset.count()

    def total_huu_adolescents(self, protocol=None):
        """Return total enrolled infant that are HUU adolescents.
        Total returned is for a protocol specified.
        """
        screening_identifiers = SubjectConsent.objects.values_list(
            'screening_identifier', flat=True).filter(
                child_age_at_enrollment__gte=9.5)
        
        study_child_identifiers = MaternalDataset.objects.values_list(
            'study_child_identifier', flat=True).filter(
                screening_identifier__in=screening_identifiers)
        
        child_dataset = ChildDataset.objects.filter(
            study_child_identifiers__in=study_child_identifiers,
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
        if (self.age_at_enrollment() <= 2.5 and self.protocol == 'Tshilo Dikotla' and
                self.total_HEU(protocol='Tshilo Dikotla') < 200 and
                self.total_HUU(protocol='Tshilo Dikotla') < 175 and self.age_at_year_3 <= 4.5):
            return True
        return False


    def cohort_b(self):
        """Return True id an infant mother pair meets criteria for cohort B.
        """
        protocols = ['Tshilo Dikotla', 'Mpepu', 'Tshipidi']
        if (self.age_at_enrollment() >= 4 and self.age_at_enrollment() <= 8.5 and
                self.protocol in protocols and self.age_at_year_3 >= 6 and
                self.age_at_year_3 <= 10.5):
            if self.efv_regime and self.total_efv_regime < 100:
                return True
            if self.dtg_regime and self.total_dtg_regime:
                return True
            if self.no_hiv_during_preg and self.total_no_hiv_during_preg:
                return True
        return False

    def cohort_c(self):
        """Return True id an infant mother pair meets criteria for cohort C.
        """
        # TODO: cater for 125 new enrolled adolescents
        if (self.age_at_enrollment() >= 8 and self.age_at_enrollment() <= 17 and
            self.age_at_year_3 >= 10):
            if self.huu_adolescents and self.total_huu_adolescents(protocol='Mashi') < 75:
                return True
            if (self.pi_regime and self.protocol == 'Mma Bana' and
                    self.total_pi_regime(protocol='Mma Bana') < 100):
                return True
        return False

    @property
    def cohort_variable(self):
        if self.cohort_a():
            return 'cohort_a'
        elif self.cohort_b():
            return 'cohort_b'
        elif self.cohort_c():
            return 'cohort_c'
        else:
            return 'pool'
