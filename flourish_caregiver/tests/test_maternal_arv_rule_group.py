from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_caregiver.helper_classes import MaternalStatusHelper
from flourish_child.models import ChildDummySubjectConsent


@tag('arv')
class TestMaternalARVRuleGroup(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_identifier = '12345678'
        self.study_maternal_identifier = '89721'

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
            'consent_copy': YES
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

    def test_maternal_arv_during_preg_required(self):
        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.maternalarvduringpreg',
            subject_identifier=self.consent.subject_identifier,
            visit_code='1000M').entry_status, REQUIRED)

    def test_maternal_arv_during_delivery(self):
        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.consent.subject_identifier, )
        child_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=self.child_consent.subject_identifier,
        )

        child_consent.dob = (get_utcnow() - relativedelta(days=1)).date()
        child_consent.save()

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

        # CRF has been removed at delivery and replaced with
        # Maternal at delivery CRF. Assert Does not exist. (redmine 6265)
        self.assertEqual(CrfMetadata.objects.filter(
                model='flourish_caregiver.maternalarvduringpreg',
                subject_identifier=self.consent.subject_identifier,
                visit_code='2000D').count(), 0, )
