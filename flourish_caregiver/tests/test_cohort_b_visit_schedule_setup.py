from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from edc_appointment.models import Appointment

from ..models import OnScheduleCohortB


class TestInterventionVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow() - relativedelta(days=5),
            'version': '1'}

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            subject_identifier='12345678',
            **self.options)


    def test_cohort_b_onschedule_valid(self):
        self.enrollment = mommy.make_recipe(
            'flourish_caregiver.enrollment',
            subject_identifier=self.subject_consent.subject_identifier,
            have_child=YES,
            child_age='gt_3_lt_10')
        
        self.assertEqual(OnScheduleCohortB.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortB.objects.get(
            subject_identifier=self.subject_consent.subject_identifier).schedule_name, 'cohort_b_schedule_1')
        
    
    def test_cohort_a_onschedule_valid(self):
        self.enrollment = mommy.make_recipe(
            'flourish_caregiver.enrollment',
            subject_identifier=self.subject_consent.subject_identifier,
            have_child=YES,
            child_age='lt_3')
        
        self.assertEqual(OnScheduleCohortB.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortB.objects.get(
            subject_identifier=self.subject_consent.subject_identifier).schedule_name, 'cohort_a_schedule_1')
        
    
    def test_cohort_c_onschedule_valid(self):
        self.enrollment = mommy.make_recipe(
            'flourish_caregiver.enrollment',
            subject_identifier=self.subject_consent.subject_identifier,
            have_child=YES,
            child_age='gt_10')
        
        self.assertEqual(OnScheduleCohortB.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortB.objects.get(
            subject_identifier=self.subject_consent.subject_identifier).schedule_name, 'cohort_c_schedule_1')


    def test_appointments_created(self):
        """Assert that three appointments were created"""
        self.enrollment = mommy.make_recipe(
            'flourish_caregiver.enrollment',
            subject_identifier=self.subject_consent.subject_identifier,
            have_child=YES,
            child_age='gt_3_lt_10')
        
        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 3)

    