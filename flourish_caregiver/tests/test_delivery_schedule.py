from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, POS
from edc_facility.import_holidays import import_holidays
from edc_metadata import REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from ..helper_classes import MaternalStatusHelper
from ..models import OnScheduleCohortABirth


@tag('md')
class TestDeliverySchedule(TestCase):

    databases = '__all__'

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'
        }

        self.subject_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen')

        self.eligible_options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow,
            'remain_in_study': YES,
            'hiv_testing': YES,
            'breastfeed_intent': YES,
            'consent_reviewed': YES,
            'study_questions': YES,
            'assessment_score': YES,
            'consent_signature': YES,
            'consent_copy': YES,
            'version': '4'
        }
        self.consent = mommy.make_recipe('flourish_caregiver.subjectconsent',
                                         **self.eligible_options)

        self.child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.consent,
            gender=None,
            first_name=None,
            last_name=None,
            identity=None,
            confirm_identity=None,
            study_child_identifier=None,
            child_dob=None,
            preg_enroll=True,
            version='2')

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            child_subject_identifier=self.child_consent.subject_identifier,
            subject_identifier=self.consent.subject_identifier)

        self.status_helper = MaternalStatusHelper(
            subject_identifier=self.consent.subject_identifier)

        self.enrol_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='1000M',
                subject_identifier=self.consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.ultrasound',
            maternal_visit=self.enrol_visit,
            child_subject_identifier=self.child_consent.subject_identifier,
            number_of_gestations=1
        )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.child_consent.subject_identifier,
            subject_identifier=self.consent.subject_identifier)

    def test_delivery_form_valid(self):

        self.assertEqual(OnScheduleCohortABirth.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_birth1_schedule1').count(), 1)

        self.assertEqual(self.status_helper.hiv_status, POS)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.consent.subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.maternalarvatdelivery',
            subject_identifier=self.consent.subject_identifier,
            visit_code='2000D').entry_status, REQUIRED)
