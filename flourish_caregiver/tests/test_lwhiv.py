from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_caregiver.helper_classes import MaternalStatusHelper
from flourish_caregiver.models import OnScheduleCohortBSec


@tag('lwhiv')
class TestLWHIV(TestCase):

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

    def test_maternal_arv_adherence_required(self):
        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.maternalarvadherence',
            subject_identifier=self.consent.subject_identifier,
            visit_code='1000M').entry_status, REQUIRED)

    def test_maternal_arv_adherence_not_required(self):
        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=5, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '89721',
            'protocol': 'Mpepu'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '89721',
            'study_child_identifier': '1234'}

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=0,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            dob=get_utcnow() - relativedelta(years=5, months=5),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier, )

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=get_utcnow() - relativedelta(years=5, months=5), )

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(OnScheduleCohortBSec.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_sec1_schedule1').count(), 1)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.maternalarvadherence',
            subject_identifier=subject_consent.subject_identifier,
            visit_code='2000M').entry_status, NOT_REQUIRED)