from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import REQUIRED, NOT_REQUIRED
from edc_metadata.models import RequisitionMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_caregiver.models import OnScheduleCohortABirth, OnScheduleCohortAQuarterly


@tag('viral')
class TestViralLoad(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '2'
            }

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen', )

        self.preg_subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        self.preg_caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.preg_subject_consent,
            gender=None,
            first_name=None,
            last_name=None,
            identity=None,
            confirm_identity=None,
            study_child_identifier=None,
            child_dob=None,
            version='2')

        self.preg_subject_identifier = self.preg_subject_consent.subject_identifier

    @tag('bdt')
    def test_viral_load_required(self):
        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen', )

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            gender=None,
            first_name=None,
            last_name=None,
            identity=None,
            confirm_identity=None,
            study_child_identifier=None,
            child_dob=None,
            version='2')

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(OnScheduleCohortABirth.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_birth1_schedule1').count(), 1)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=subject_consent.subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            RequisitionMetadata.objects.get(
                panel_name='viral_load',
                subject_identifier=subject_consent.subject_identifier,
                visit_code='2000D').entry_status, REQUIRED)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_quarterly1_schedule1').count(), 1)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=subject_consent.subject_identifier,
                visit_code='2001M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            RequisitionMetadata.objects.get(
                panel_name='viral_load',
                subject_identifier=subject_consent.subject_identifier,
                visit_code='2001M').entry_status, NOT_REQUIRED)
