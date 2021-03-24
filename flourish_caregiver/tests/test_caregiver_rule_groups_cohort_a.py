from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, INCOMPLETE, NO
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy
from edc_appointment.models import Appointment


class TestRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            subject_identifier='12345678',
            **self.options)

        mommy.make_recipe(
           'flourish_caregiver.antenatalenrollment',
           subject_identifier=self.subject_consent.subject_identifier,)


        self.appointment_1000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='1000M')

        self.subject_visit_1000 = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=2),
            appointment=self.appointment_1000)


    @tag('a')
    def test_hiv_viralload_cd4_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivviralloadandcd4',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)


    @tag('a')
    def test_arvsprepregnancy_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.arvsprepregnancy',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)


    @tag('a')
    def test_arvsduringpregnancy_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.arvsduringpregnancy',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('a')
    def test_caregiverphqdeprscreening_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqdeprscreening',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('a')
    def test_caregiverhamddeprscreening_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverhamddeprscreening',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)


    @tag('a')
    def test_caregiveredinburghdeprscreening_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiveredinburghdeprscreening',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('a')
    def test_ultrasound_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.ultrasound',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)



