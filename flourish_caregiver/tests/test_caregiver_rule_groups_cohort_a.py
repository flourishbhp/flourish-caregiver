from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from ..models import MaternalVisit


@tag('mtd')
class TestRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'breastfeed_intent': YES,
            'version': '1'}

        self.screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen')

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=self.screening_preg.screening_identifier,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=self.subject_consent.subject_identifier,)

        self.subject_identifier = self.subject_consent.subject_identifier

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(visit_code='1000M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_hiv_viralload_cd4_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivviralloadandcd4',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_arvsprepregnancy_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.arvsprepregnancy',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_arvsduringpregnancy_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.maternalarvduringpreg',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_caregiverphqdeprscreening_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqdeprscreening',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    def test_caregiveredinburghdeprscreening_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiveredinburghdeprscreening',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_ultrasound_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.ultrasound',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_gad_scoregte_10_referral_required(self):
        visit = MaternalVisit.objects.get(visit_code='1000M')
        mommy.make_recipe('flourish_caregiver.gadanxietyscreening',
                          maternal_visit=visit)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregivergadreferral',
                subject_identifier=self.subject_identifier,
                visit_code='1000M').entry_status, REQUIRED)

    def test_phq9gte_5_referral_required(self):
        visit = MaternalVisit.objects.get(visit_code='1000M')
        mommy.make_recipe('flourish_caregiver.caregiverphqdeprscreening',
                          maternal_visit=visit)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqreferral',
                subject_identifier=self.subject_identifier,
                visit_code='1000M').entry_status, REQUIRED)

    @tag('arr')
    def test_edingte_10_referral_required(self):
        visit = MaternalVisit.objects.get(
            visit_code='1000M', visit_code_sequence='0')
        mommy.make_recipe('flourish_caregiver.caregiveredinburghdeprscreening',
                          maternal_visit=visit)
        import pdb; pdb.set_trace()
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiveredinburghreferral',
                subject_identifier=self.subject_identifier,
                visit_code='1000M').entry_status, REQUIRED)
