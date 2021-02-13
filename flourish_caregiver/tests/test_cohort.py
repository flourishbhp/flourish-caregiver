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
        self.assertEquals(cohort.age_at_enrollment, 2.0)

    def test_calculate_age2(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=2, months=5),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertEquals(cohort.age_at_enrollment, 2.5)

    def test_find_age(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=2, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla'
            )
        self.assertEquals(cohort.age_at_enrollment, 2.7)

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
        
    def test_hiv_unexposed_uninfacted(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=2, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Unexposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertTrue(cohort.hiv_unexposed_uninfacted)

    def test_hiv_unexposed_uninfacted2(self):
        cohort = Cohort(
            child_dob=date.today() - relativedelta(years=2, months=7),
            enrollment_date=timezone.now().date(),
            infant_hiv_exposed='Exposed',
            mum_hiv_status='HIV-infected',
            protocol='Tshilo Dikotla')
        self.assertFalse(cohort.hiv_unexposed_uninfacted)

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