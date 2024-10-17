from dateutil.relativedelta import relativedelta
from django.test import tag, TestCase
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import YES, NO
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED
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
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregivertbscreening',
                subject_identifier=self.subject_identifier,
                visit_code='2001M').entry_status, REQUIRED)

    def test_screening_2weeks_call_required(self):
        """ Assert 2weeks unscheduled appointment created
            when symptomatic at quarterly call.
        """
        mommy.make_recipe(
            'flourish_caregiver.caregivertbscreening',
            maternal_visit=self.visit_2001,
            report_datetime=get_utcnow(),
            cough=YES,
            household_diagnosed_with_tb=NO,
            evaluated_for_tb=NO)

        self.assertEqual(
            Appointment.objects.filter(
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_2001.visit_code,
                visit_code_sequence=1).count(), 1)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_2001.visit_code,
                visit_code_sequence=1),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregivertbscreening',
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_2001.visit_code,
                visit_code_sequence=1).entry_status, REQUIRED)

    def test_tb_referral_required(self):
        """ Check TB Referral required for quarterly call,
            when there's a household contact and there's
            no 2 week call scheduled.
        """
        mommy.make_recipe(
            'flourish_caregiver.caregivertbscreening',
            maternal_visit=self.visit_2001,
            report_datetime=get_utcnow(),
            fever=YES,
            household_diagnosed_with_tb=YES,
            evaluated_for_tb=NO, )

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.tbreferralcaregiver',
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_2001.visit_code).entry_status, REQUIRED)

        self.assertEqual(
            Appointment.objects.filter(
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_2001.visit_code,
                visit_code_sequence=1).count(), 0)

    def test_tb_referral_2weeks_required(self):
        """ Check TB Referral required for 2 weeks FU call,
            when there's persistent symptoms.
        """
        mommy.make_recipe(
            'flourish_caregiver.caregivertbscreening',
            maternal_visit=self.visit_2001,
            report_datetime=get_utcnow(),
            fever=YES,
            household_diagnosed_with_tb=NO,
            evaluated_for_tb=NO, )

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.tbreferralcaregiver',
            subject_identifier=self.subject_identifier,
            visit_code=self.visit_2001.visit_code).entry_status, NOT_REQUIRED)

        self.assertEqual(
            Appointment.objects.filter(
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_2001.visit_code,
                visit_code_sequence=1).count(), 1)

        visit_2week = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_2001.visit_code,
                visit_code_sequence=1),
            report_datetime=get_utcnow(),
            reason=UNSCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.caregivertbscreening',
            maternal_visit=visit_2week,
            report_datetime=get_utcnow(),
            fever=YES,
            household_diagnosed_with_tb=NO,
            evaluated_for_tb=NO, )

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.tbreferralcaregiver',
                subject_identifier=self.subject_identifier,
                visit_code=visit_2week.visit_code,
                visit_code_sequence=1).entry_status, REQUIRED)

    def test_tb_referral_not_required(self):
        """ Check TB Referral not required for quarterly call,
            when there's NO household contact.
        """
        mommy.make_recipe(
            'flourish_caregiver.caregivertbscreening',
            maternal_visit=self.visit_2001,
            report_datetime=get_utcnow(),
            fever=YES,
            household_diagnosed_with_tb=NO,
            evaluated_for_tb=NO, )

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.tbreferralcaregiver',
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_2001.visit_code).entry_status, NOT_REQUIRED)

    def test_tb_referral_2weeks_not_required(self):
        """ Check TB Referral not required at 2 week FU call,
            when there's no persistent symptoms.
        """
        mommy.make_recipe(
            'flourish_caregiver.caregivertbscreening',
            maternal_visit=self.visit_2001,
            report_datetime=get_utcnow(),
            fever=YES,
            household_diagnosed_with_tb=NO,
            evaluated_for_tb=NO, )

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.tbreferralcaregiver',
            subject_identifier=self.subject_identifier,
            visit_code=self.visit_2001.visit_code).entry_status, NOT_REQUIRED)

        self.assertEqual(
            Appointment.objects.filter(
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_2001.visit_code,
                visit_code_sequence=1).count(), 1)

        visit_2week = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_2001.visit_code,
                visit_code_sequence=1),
            report_datetime=get_utcnow(),
            reason=UNSCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.caregivertbscreening',
            maternal_visit=visit_2week,
            report_datetime=get_utcnow(),
            fever=NO,
            household_diagnosed_with_tb=NO,
            evaluated_for_tb=NO, )

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.tbreferralcaregiver',
                subject_identifier=self.subject_identifier,
                visit_code=visit_2week.visit_code,
                visit_code_sequence=1).entry_status, REQUIRED)

    def test_tb_referral_outcome_required(self):
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

    def test_tb_referral_outcome_not_required(self):
        mommy.make_recipe(
            'flourish_caregiver.tbreferralcaregiver',
            maternal_visit=self.visit_2001,
            report_datetime=get_utcnow())

        visit_2002 = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2002M',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.caregivertbreferraloutcome',
            maternal_visit=visit_2002,
            report_datetime=get_utcnow())

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2003M',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.caregivertbreferraloutcome',
            subject_identifier=self.subject_identifier,
            visit_code='2003M').entry_status, NOT_REQUIRED)
