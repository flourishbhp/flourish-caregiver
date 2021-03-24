from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, INCOMPLETE, NO
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy


@tag('mtd')
class TestRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.subject_identifier = '12345678'

        self.options = {
            'consent_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'version': '1'}

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier,)

    @tag('a')
    def test_hiv_viralload_cd4_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivviralloadandcd4',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('a')
    def test_arvsprepregnancy_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.arvsprepregnancy',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('a')
    def test_arvsduringpregnancy_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.arvsduringpregnancy',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('a')
    def test_caregiverphqdeprscreening_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqdeprscreening',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('a')
    def test_caregiverhamddeprscreening_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverhamddeprscreening',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('a')
    def test_caregiveredinburghdeprscreening_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiveredinburghdeprscreening',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('a')
    def test_ultrasound_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.ultrasound',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

