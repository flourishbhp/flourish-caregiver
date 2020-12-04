from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from edc_appointment.models import Appointment

from ..models import OnScheduleCohortA


class TestVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}        
    
    def test_cohort_a_onschedule_valid(self):
        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            subject_identifier='12345678',
            **self.options)
        
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier,)
        
        self.assertEqual(OnScheduleCohortA.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortA.objects.get(
            subject_identifier=subject_consent.subject_identifier).schedule_name, 'cohort_a_schedule_1')
         
         
        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 3)

    
