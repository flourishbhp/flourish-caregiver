from django.test import tag, TestCase
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import NO, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_caregiver.subject_helper_mixin import SubjectHelperMixin


@tag('tbro')
class TestTBReferralOutcome(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_helper = SubjectHelperMixin()

        self.subject_identifier = self.subject_helper.create_antenatal_enrollment(
            version='3')

        self.caregiver_visit_1000M = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='1000M',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_tb_referral_outcome_required(self):
        self.assertEqual(CrfMetadata.objects.get(
            subject_identifier=self.subject_identifier,
            model='flourish_caregiver.caregivertbreferraloutcome',
            visit_code='1000M').entry_status, NOT_REQUIRED)

        tb_referral_caregiver = mommy.make_recipe(
            'flourish_caregiver.tbreferralcaregiver',
            maternal_visit=self.caregiver_visit_1000M,
            referred_for_screening=YES)
        tb_referral_caregiver.save()

        self.assertEqual(CrfMetadata.objects.get(
            subject_identifier=self.subject_identifier,
            model='flourish_caregiver.caregivertbreferraloutcome',
            visit_code='1000M').entry_status, REQUIRED)

    def test_tb_referral_outcome_not_required(self):
        self.assertEqual(CrfMetadata.objects.get(
            subject_identifier=self.subject_identifier,
            model='flourish_caregiver.caregivertbreferraloutcome',
            visit_code='1000M').entry_status, NOT_REQUIRED)

        mommy.make_recipe(
            'flourish_caregiver.tbreferralcaregiver',
            maternal_visit=self.caregiver_visit_1000M,
            referred_for_screening=NO)

        self.assertEqual(CrfMetadata.objects.get(
            subject_identifier=self.subject_identifier,
            model='flourish_caregiver.caregivertbreferraloutcome',
            visit_code='1000M').entry_status, NOT_REQUIRED)
