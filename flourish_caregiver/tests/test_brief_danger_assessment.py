from django.test import tag, TestCase
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_caregiver.subject_helper_mixin import SubjectHelperMixin


@tag('bda')
class TestBriefDangerAssessment(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_helper = SubjectHelperMixin()

        self.subject_identifier = self.subject_helper.create_antenatal_enrollment(
            version='3'
        )

        self.enrol_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='1000M',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_brief_danger_assessment_required(self):
        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.briefdangerassessment',
            subject_identifier=self.subject_identifier,
            visit_code='1000M').entry_status, NOT_REQUIRED)

        hits_screening_obj = mommy.make_recipe(
            'flourish_caregiver.hitsscreening',
            maternal_visit=self.enrol_visit,
            physical_hurt='1',
            insults='1',
            threaten='1',
            screem_curse='1',
        )

        self.assertEqual(hits_screening_obj.score, 4)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.briefdangerassessment',
            subject_identifier=self.subject_identifier,
            visit_code='1000M').entry_status, NOT_REQUIRED)

    def test_brief_danger_assessment_not_required(self):
        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.briefdangerassessment',
            subject_identifier=self.subject_identifier,
            visit_code='1000M').entry_status, NOT_REQUIRED)

        hits_screening_obj = mommy.make_recipe(
            'flourish_caregiver.hitsscreening',
            maternal_visit=self.enrol_visit,
            physical_hurt='5',
            insults='5',
            threaten='5',
            screem_curse='5',
        )

        self.assertEqual(hits_screening_obj.score, 20)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.briefdangerassessment',
            subject_identifier=self.subject_identifier,
            visit_code='1000M').entry_status, REQUIRED)
