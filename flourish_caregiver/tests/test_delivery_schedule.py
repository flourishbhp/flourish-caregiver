from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from edc_constants.constants import YES
from ..models import OnScheduleCohortABirth, OnScheduleCohortAQuarterly


@tag('md')
class TestDeliverySchedule(TestCase):

    databases = '__all__'

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

    def test_delivery_form_valid(self):

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier,)

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(OnScheduleCohortABirth.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_birth1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_quarterly1_schedule1').count(), 1)
