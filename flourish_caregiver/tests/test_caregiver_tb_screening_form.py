from dateutil.relativedelta import relativedelta
from django.test import tag, TestCase
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import PENDING, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_caregiver.models import OnScheduleCohortAAntenatal, SubjectConsent
from flourish_caregiver.subject_helper_mixin import SubjectHelperMixin


@tag('ctbsf')
class TestCaregiverTbScreeningForm(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_helper = SubjectHelperMixin()

        self.subject_identifier = self.subject_helper.create_antenatal_enrollment(
            version='4'
        )

        self.caregiver_onschedule = OnScheduleCohortAAntenatal.objects.get(
            subject_identifier=self.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.subject_identifier,
            child_subject_identifier=self.caregiver_onschedule.child_subject_identifier,
            delivery_datetime=get_utcnow() - relativedelta(days=1),
        )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.caregiver_onschedule.child_subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(),
            user_created='imosweu')

        self.subject_consent = SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier
        )

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000D',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.visit_2001 = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2001M',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_tb_screening_form_required(self):
        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.caregivertbscreening',
            subject_identifier=self.subject_identifier,
            visit_code='2001M').entry_status, REQUIRED)

        mommy.make_recipe(
            'flourish_caregiver.caregivertbscreening',
            maternal_visit=self.visit_2001,
            report_datetime=get_utcnow(),
            chest_xray_results=PENDING, )

        self.visit_2001 = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2002M',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.caregivertbscreening',
            subject_identifier=self.subject_identifier,
            visit_code='2002M').entry_status, REQUIRED)

    @tag('ctbro')
    def test_caregiver_tb_referral_outcome_form_required(self):
        mommy.make_recipe(
            'flourish_caregiver.tbreferralcaregiver',
            maternal_visit=self.visit_2001,
            report_datetime=get_utcnow())

        self.visit_2001 = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2002M',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.caregivertbreferraloutcome',
            subject_identifier=self.subject_identifier,
            visit_code='2002M').entry_status, REQUIRED)

    def test_tb_referral_required(self):

        mommy.make_recipe(
            'flourish_caregiver.caregivertbscreening',
            maternal_visit=self.visit_2001,
            fever=YES,
            tb_diagnoses=True,
            report_datetime=get_utcnow())

        mommy.make_recipe(
            'flourish_caregiver.tbreferralcaregiver',
            maternal_visit=self.visit_2001,
            report_datetime=get_utcnow())

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2002M',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.caregivertbreferraloutcome',
            subject_identifier=self.subject_identifier,
            visit_code='2002M').entry_status, REQUIRED)

    def test_tb_referral_not_required(self):

        self.visit_2001 = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2002M',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.caregivertbscreening',
            maternal_visit=self.visit_2001,
            report_datetime=get_utcnow())

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.caregivertbreferraloutcome',
            subject_identifier=self.subject_identifier,
            visit_code='2002M').entry_status, NOT_REQUIRED)
