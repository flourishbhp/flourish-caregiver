from dateutil.relativedelta import relativedelta
from django.test import tag, TestCase
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import NO, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy


@tag('post_hiv_test')
class TestPostHIVTest(TestCase):

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

        self.maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=2, months=5),
            **self.child_dataset_options)

    def test_post_hiv_test_required(self):
        """Test post hiv test crf metadata is required when a caregiver is a biological
        mother."""
        screening_obj = mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            mother_alive=YES,
            flourish_participation='interested')

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_obj.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=(get_utcnow() - relativedelta(years=4, months=5)).date(), )

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2001M',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            subject_identifier=subject_consent.subject_identifier,
            model='flourish_caregiver.posthivrapidtestandconseling',
            visit_code='2001M').entry_status, REQUIRED)

    def test_post_hiv_test_not_required(self):
        """Test post hiv test crf metadata is not required when a caregiver is not a
        biological mother."""
        screening_obj = mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            mother_alive=NO,
            flourish_participation='interested')

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_obj.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=NO,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=(get_utcnow() - relativedelta(years=4, months=5)).date(), )

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2001M',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            subject_identifier=subject_consent.subject_identifier,
            model='flourish_caregiver.posthivrapidtestandconseling',
            visit_code='2001M').entry_status, NOT_REQUIRED)
