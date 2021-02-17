from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from edc_appointment.models import Appointment

from ..models import OnScheduleCohortA, OnScheduleCohortB, OnScheduleCohortC
from ..models import OnSchedulePool


@tag('vs')
class TestVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

    def test_cohort_a_onschedule_antenatal_valid(self):
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
            subject_identifier=subject_consent.subject_identifier).count(), 4)

    def test_cohort_a_onschedule_consent_valid(self):
        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            subject_identifier='12345678',
            **self.options)

        subject_consent.cohort = 'cohort_a'
        subject_consent.save()

        self.assertEqual(OnScheduleCohortA.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortA.objects.get(
            subject_identifier=subject_consent.subject_identifier).schedule_name,
            'cohort_a_schedule_1')

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 4)

    def test_cohort_b_onschedule_valid(self):
        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            subject_identifier='12345678',
            **self.options)

        subject_consent.cohort = 'cohort_b'
        subject_consent.save()

        self.assertEqual(OnScheduleCohortB.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortB.objects.get(
            subject_identifier=subject_consent.subject_identifier).schedule_name,
            'cohort_b_schedule_1')

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 3)

    def test_cohort_c_onschedule_valid(self):
        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            subject_identifier='12345678',
            ** self.options)

        subject_consent.cohort = 'cohort_c'
        subject_consent.save()

        self.assertEqual(OnScheduleCohortC.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortC.objects.get(
            subject_identifier=subject_consent.subject_identifier).schedule_name,
            'cohort_c_schedule_1')

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 3)

    def test_pool_onschedule_valid(self):
        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            subject_identifier='12345678',
            ** self.options)

        subject_consent.cohort = 'pool'
        subject_consent.save()

        self.assertEqual(OnSchedulePool.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnSchedulePool.objects.get(
            subject_identifier=subject_consent.subject_identifier).schedule_name,
            'pool_schedule_1')

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)
