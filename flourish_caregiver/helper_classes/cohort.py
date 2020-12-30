

class CohortError(Exception):
    pass


class Cohort:

    """Class that determines the cohort that a child belong too
    """

    def __init__(
            self, child_dob=None, enrollment_date=None, infant_hiv_exposed=None,
            mum_hivstatus=None, protocol=None):

        self.child_dob = child_dob
        self.enrollment_date = enrollment_date
        self.infant_hiv_exposed = infant_hiv_exposed
        self.mum_hivstatus = mum_hivstatus
        self.protocol = protocol

    @property
    def age_at_enrollment(self):
        return self.enrollment_date.year - self.child_dob.year - (
                (self.enrollment_date.month, self.enrollment_date.day) < (
            self.child_dob.month, self.child_dob.day))

    @property
    def hiv_exposed_uninfected(self,):
        """Return True is an infant is HEU.
        """
        if self.infant_hiv_exposed == 'Exposed':
            return True
        return False

    @property
    def hiv_unexposed_uninfacted(self):
        """Returns True if an infant is HUU
        """
        if self.infant_hiv_exposed == 'Unexposed':
            return True
        return False

    @property
    def huu_adolescents(self):
        """Returns True if the infant is HUU and is an Adolescent.
        """
        if self.age_at_enrollment >= 10 and self.hiv_unexposed_uninfacted:
            return True
        return False

    @property
    def no_hiv_during_preg(self):
        """Return True if the infant had no expore to HIV during pregnancy.
        """
        if self.mom_hivstatus == 'HIV uninfected':
            return True
        return False

    property
    def efv_regime(self):
        """."""
        return False

    @property
    def dtg_regime(self):
        """."""
        return False

    @property
    def pi_regime(self):
        """."""
        return True

    @property
    def total_efv_regime(self):
        """Return total enrolled infant for a specified protocol with EFV regime.
        """
        return 0

    @property
    def total_dtg_regime(self):
        """Return total enrolled infant for a specified protocol with DTG regime.
        """
        return 0

    @property
    def total_pi_regime(self):
        """Returns total enrolled infants for a specified protocol with PI regime.
        """
        return 0

    def total_HEU(self, protocol=None):
        """Return total enrolled Tshilo Dikotla HEU.
        """
        return 0

    @property
    def total_no_hiv_during_preg(self):
        """Return total number of infants with no HIV expore.
        """
        return 0

    def total_HUU(self, protocol=None):
        """Returns total enrolled Tshilo Dikotla HUU infants.
        """
        return 0

    def total_huu_adolescents(self, protocol=None):
        """Return total enrolled infant that are HUU adolescents.
        Total returned is for a protocol specified.
        """
        return 0

    def cohort_a(self):
        """Return True if the infant mother pair meets criteria for cohort A.
        """
        #TODO: Cater for 200 newly enrolled pregnant woman.
        if (self.age_at_enrollment <= 3 and self.protocol == 'Tshilo Dikotla' and
                self.total_HEU(protocol='Tshilo Dikotla') < 200 and self.total_HUU(protocol='Tshilo Dikotla') < 175):
            return True
        return False


    def cohort_b(self):
        """Return True id an infant mother pair meets criteria for cohort B.
        """
        protocols = ['Tshilo Dikotla', 'Mpepu', 'Tshipidi']
        if (self.age_at_enrollment >= 4 and self.age_at_enrollment <= 9 and
                self.protocol in protocols):
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
        #TODO: cater for 125 new enrolled adolescents
        if self.age_at_enrollment >= 10:
            if self.huu_adolescents and self.total_huu_adolescents(protocol='Mashi') < 75:
                return True
            if (self.pi_regime and self.protocol == 'Mma Bana' and
                    self.total_pi_regime(protocol='Mma Bana') < 100):
                return True
        return False
