from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.test import TestCase
from django.test.utils import tag
from edc_appointment.constants import IN_PROGRESS_APPT
from edc_appointment.models import Appointment
from edc_action_item.models.action_item import ActionItem
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, OPEN, NEW
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import SCHEDULED

from model_mommy import mommy
from ..identifiers import ScreeningIdentifier


@tag('offstudy')
class TestOffStudyAction(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        screening_identifier = ScreeningIdentifier().identifier

        mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=screening_identifier,
            version='1',
            child_version='1')

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',
            screening_identifier=screening_identifier)

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        self.child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            gender=None,
            first_name=None,
            last_name=None,
            identity=None,
            confirm_identity=None,
            study_child_identifier=None,
            child_dob=None,
            preg_enroll=True,
            version='1')

    def test_ultrasound_triggers_offstudy(self):

        subject_identifier = self.subject_consent.subject_identifier
        options = {
            'subject_identifier': subject_identifier,
            'edd_by_lmp': None}

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            child_subject_identifier=self.child_consent.subject_identifier,
            **options)

        self.assertEqual(ActionItem.objects.filter(
            subject_identifier=subject_identifier,
            reference_model='flourish_prn.caregiveroffstudy',
            status='New').count(), 0)

        appointment_1000M = Appointment.objects.get(
            visit_code='1000M',
            subject_identifier=subject_identifier)

        appointment_1000M.appt_status = IN_PROGRESS_APPT
        appointment_1000M.save()

        maternal_visit_1000M = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=appointment_1000M,
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.ultrasound',
            child_subject_identifier=self.child_consent.subject_identifier,
            maternal_visit=maternal_visit_1000M,
            report_datetime=get_utcnow(),
            number_of_gestations=1,
            est_edd_ultrasound=(get_utcnow() + relativedelta(months=7)).date())

        self.assertEqual(ActionItem.objects.filter(
            Q(status=OPEN) | Q(status=NEW),
            subject_identifier=subject_identifier,
            reference_model='flourish_prn.caregiveroffstudy',).count(), 1)
