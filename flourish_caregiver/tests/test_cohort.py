from dateutil.relativedelta import relativedelta
from datetime import date

from django.test.testcases import TestCase
from  django.utils import timezone

from ..helper_classes import Cohort


class TestCohort(TestCase):

    def setUp(self):
        pass

    def test_calculate_age1(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=2),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertEquals(cohort.age_at_enrollment(), 2.0)

    def test_calculate_age2(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=2, months=5),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertEquals(cohort.age_at_enrollment(), 2.5)

    def test_calculate_age3(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=2, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla'
            )
        self.assertEquals(cohort.age_at_enrollment(), 2.7)

    def test_hiv_exposed_uninfected(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=2, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertTrue(cohort.hiv_exposed_uninfected)

    def test_hiv_exposed_uninfected2(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=2, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Unexposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertFalse(cohort.hiv_exposed_uninfected)

    def test_hiv_unexposed_uninfected(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=2, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Unexposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertTrue(cohort.hiv_unexposed_uninfected)

    def test_hiv_unexposed_uninfected2(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=2, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertFalse(cohort.hiv_unexposed_uninfected)

    def test_huu_adolescents(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Unexposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertTrue(cohort.huu_adolescents)

    def test_huu_adolescents2(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertFalse(cohort.huu_adolescents)

    def test_huu_adolescents3(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=3, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertFalse(cohort.huu_adolescents)

    def test_huu_adolescents4(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=3, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Unexposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertFalse(cohort.huu_adolescents)

    def test_no_hiv_during_preg(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV uninfected',
            protocol='Tshilo Dikotla')
        self.assertTrue(cohort.no_hiv_during_preg)

    def test_pi(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV uninfected',
            protocol='Tshilo Dikotla',
            pi=1)
        self.assertTrue(cohort.pi_regime)

    def test_pi2(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV uninfected',
            protocol='Tshilo Dikotla',
            pi=0)
        self.assertFalse(cohort.pi_regime)

    def test_pi3(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV uninfected',
            protocol='Tshilo Dikotla')
        self.assertFalse(cohort.pi_regime)

    def test_efv(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV uninfected',
            protocol='Tshilo Dikotla',
            efv=1)
        self.assertTrue(cohort.efv_regime)

    def test_efv2(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV uninfected',
            protocol='Tshilo Dikotla',
            efv=0)
        self.assertFalse(cohort.efv_regime)

    def test_efv3(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV uninfected',
            protocol='Tshilo Dikotla')
        self.assertFalse(cohort.efv_regime)

    def test_dtg(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV uninfected',
            protocol='Tshilo Dikotla',
            dtg=1)
        self.assertTrue(cohort.dtg_regime)

    def test_dtg2(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV uninfected',
            protocol='Tshilo Dikotla',
            dtg=0)
        self.assertFalse(cohort.dtg_regime)

    def test_dtg3(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=10, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV uninfected',
            protocol='Tshilo Dikotla')
        self.assertFalse(cohort.dtg_regime)
