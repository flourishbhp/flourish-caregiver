from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from edc_appointment.models import Appointment

from ..models import OnScheduleCohortA, OnSchedulePreFlourish


class TestVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow() - relativedelta(days=5),
            'version': '1'}

    @tag('pf')
    def test_pre_flourish_onschedule_valid(self):
        pre_flourish_consent = mommy.make_recipe(
            'flourish_caregiver.preflourishconsent',
            pre_flourish_identifier='12345678',
            **self.options)
        
        self.assertEqual(OnSchedulePreFlourish.objects.filter(
            subject_identifier=pre_flourish_consent.pre_flourish_identifier).count(), 1)

        self.assertEqual(OnSchedulePreFlourish.objects.get(
            subject_identifier=pre_flourish_consent.pre_flourish_identifier).schedule_name, 'pre_flourish_schedule_1')
        
        self.assertEqual(Appointment.objects.filter(
            subject_identifier=pre_flourish_consent.pre_flourish_identifier).count(), 1)
        
    
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
            subject_identifier=self.subject_consent.subject_identifier).count(), 3)

    