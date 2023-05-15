from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_caregiver.helper_classes.fu_onschedule_helper import FollowUpEnrolmentHelper
from flourish_caregiver.models import OnScheduleCohortAFU
from flourish_caregiver.subject_helper_mixin import SubjectHelperMixin


@tag('phq9')
class TestPHQ9(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_identifier = '12345678'
        self.study_maternal_identifier = '89721'

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        self.subject_identifier = self.subject_identifier[:-1] + '1'

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=2, months=5),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier, )

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            subject_identifier=self.subject_identifier,
            breastfeed_intent=YES,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=(get_utcnow() - relativedelta(years=4, months=5)).date(), )

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=self.subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=self.subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2001M',
                subject_identifier=self.subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        schedule_enrol_helper = FollowUpEnrolmentHelper(
            subject_identifier=self.subject_identifier,
            cohort='a')

        schedule_enrol_helper.activate_fu_schedule()

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='3000M',
                subject_identifier=self.subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_phq9_depression_required(self):
        self.assertEqual(OnScheduleCohortAFU.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            schedule_name='a_fu1_schedule1').count(), 1)

        self.assertEqual(CrfMetadata.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            model='flourish_caregiver.caregiverphqdeprscreening',
            visit_code='3000M').entry_status, REQUIRED)
