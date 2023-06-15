from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NEW
from edc_facility.import_holidays import import_holidays
from edc_metadata import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_schedule import site_visit_schedules
from edc_visit_schedule.models import SubjectScheduleHistory
from model_mommy import mommy

from edc_action_item.site_action_items import site_action_items
from edc_appointment.models import Appointment
from edc_visit_tracking.constants import SCHEDULED
from flourish_child.models import ChildDummySubjectConsent

from ..helper_classes import MaternalStatusHelper
from ..models.onschedule import OnScheduleCohortATb2Months, OnScheduleCohortATb6Months


@tag('tb')
class TestVisitScheduleTb(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_identifier = '12345678'
        self.study_maternal_identifier = '89721'

        self.user = mommy.make('User',
                               username='Megan',
                               is_active=True)
        self.user.set_password('password')
        self.user.save()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '3'
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
            'version': '3'
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

    def test_put_on_tb_schedule(self):
        """
        Test if a subject is put the tb schedule successfully
        """
        mommy.make_recipe(
            'flourish_caregiver.tbinformedconsent',
            subject_identifier=self.consent.subject_identifier,
            consent_datetime=get_utcnow()
        )
        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_2_months_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.consent.subject_identifier, )

        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_2_months_schedule1').count(), 1)

    @tag('tb_off')
    def test_tb_referral_required(self):
        """
        Test if the off study crf successfully removes an individul from the Tb schedule
        """
        mommy.make_recipe(
            'flourish_caregiver.tbinformedconsent',
            subject_identifier=self.consent.subject_identifier,
            consent_datetime=get_utcnow()
        )
        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_2_months_schedule1').count(), 0)

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

        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_2_months_schedule1').count(), 1)

        tb_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.consent.subject_identifier,
                visit_code='2100T'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.tbreferral',
            subject_identifier=self.consent.subject_identifier,
            visit_code='2100T').entry_status, NOT_REQUIRED)

        mommy.make_recipe('flourish_caregiver.tbvisitscreeningwomen',
                          have_cough=YES,
                          maternal_visit=tb_visit)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.tbreferral',
            subject_identifier=self.consent.subject_identifier,
            visit_code='2100T').entry_status, REQUIRED)

    def test_tb_screening_form_enrol_visit(self):
        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.tbstudyeligibility',
            subject_identifier=self.consent.subject_identifier,
            visit_code='1000M').entry_status, NOT_REQUIRED)

        mommy.make_recipe('flourish_caregiver.ultrasound',
                          maternal_visit=self.enrol_visit,
                          est_edd_ultrasound=get_utcnow().date(),
                          ga_confirmed=22)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.tbstudyeligibility',
            subject_identifier=self.consent.subject_identifier,
            visit_code='1000M').entry_status, REQUIRED)

    @tag('tb-scre')
    def test_tb_screening_form_devlivery_visit(self):
        mommy.make_recipe('flourish_caregiver.ultrasound',
                          maternal_visit=self.enrol_visit,
                          est_edd_ultrasound=get_utcnow().date(),
                          ga_confirmed=22)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.tbstudyeligibility',
            subject_identifier=self.consent.subject_identifier,
            visit_code='1000M').entry_status, REQUIRED)

        mommy.make_recipe('flourish_caregiver.tbstudyeligibility',
                          maternal_visit=self.enrol_visit,
                          reasons_not_participating='still_think')

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
            model='flourish_caregiver.tbstudyeligibility',
            subject_identifier=self.consent.subject_identifier,
            visit_code='2000D').entry_status, REQUIRED)

    @tag('off-study-tb')
    def test_tb_off_study_required(self):
        self.prepare_off_study_2_months_visit()

        tb_off_study_cls = django_apps.get_model(
            'flourish_caregiver.tboffstudy'
        )

        action_cls = site_action_items.get(tb_off_study_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.consent.subject_identifier,
                action_type__name=tb_off_study_cls.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            self.fail('Action Item to created')
            self.assertNotIsInstance(obj=action_item_obj, cls=action_item_model_cls)

    @tag('off-study-tb')
    def test_tb_off_study_functionality(self):
        self.prepare_off_study_2_months_visit()
        mommy.make_recipe('flourish_caregiver.tboffstudy',
                          subject_identifier=self.consent.subject_identifier, )

    @tag('tb6')
    def test_6_month_visit_invalid(self):
        mommy.make_recipe(
            'flourish_caregiver.tbinformedconsent',
            subject_identifier=self.consent.subject_identifier,
            consent_datetime=get_utcnow()
        )

        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_2_months_schedule1').count(), 0)

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

        tb_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.consent.subject_identifier,
                visit_code='2100T'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe('flourish_caregiver.tbvisitscreeningwomen',
                          have_cough=NO,
                          fever=NO,
                          night_sweats=NO,
                          weight_loss=NO,
                          cough_blood=NO,
                          cough_duration=None,
                          enlarged_lymph_nodes=NO,
                          maternal_visit=tb_visit)

        self.assertEqual(OnScheduleCohortATb6Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_6_months_schedule1').count(), 0)

    @tag('tb6')
    def test_6_month_visit_valid(self):
        mommy.make_recipe(
            'flourish_caregiver.tbinformedconsent',
            subject_identifier=self.consent.subject_identifier,
            consent_datetime=get_utcnow()
        )

        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_2_months_schedule1').count(), 0)

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

        tb_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.consent.subject_identifier,
                visit_code='2100T'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe('flourish_caregiver.tbvisitscreeningwomen',
                          have_cough=YES,
                          maternal_visit=tb_visit)

        self.assertEqual(OnScheduleCohortATb6Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_6_months_schedule1').count(), 1)

    @tag('tbeng')
    def test_6_month_interview_valid(self):
        mommy.make_recipe(
            'flourish_caregiver.tbinformedconsent',
            subject_identifier=self.consent.subject_identifier,
            consent_datetime=get_utcnow()
        )

        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_2_months_schedule1').count(), 0)

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

        tb_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.consent.subject_identifier,
                visit_code='2100T'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe('flourish_caregiver.tbvisitscreeningwomen',
                          have_cough=YES,
                          maternal_visit=tb_visit)

        tb_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.consent.subject_identifier,
                visit_code='2200T'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe('flourish_caregiver.tbengagement',
                          maternal_visit=tb_visit,
                          interview_consent=YES)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.tbinterview',
                subject_identifier=self.consent.subject_identifier,
                visit_code='2200T',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('6_months_offstudy')
    def test_tb_6_months_offstudy(self):
        mommy.make_recipe(
            'flourish_caregiver.tbinformedconsent',
            subject_identifier=self.consent.subject_identifier,
            consent_datetime=get_utcnow()
        )

        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_2_months_schedule1').count(), 0)

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

        tb_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.consent.subject_identifier,
                visit_code='2100T'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe('flourish_caregiver.tbvisitscreeningwomen',
                          have_cough=YES,
                          maternal_visit=tb_visit)
        schedule_history = SubjectScheduleHistory.objects.get(
            schedule_name='a_tb1_6_months_schedule1',
            onschedule_model='flourish_caregiver.onschedulecohortatb6months',
            subject_identifier=self.consent.subject_identifier
        )
        self.assertIsNone(schedule_history.offschedule_datetime)
        mommy.make_recipe('flourish_caregiver.tboffstudy',
                          subject_identifier=self.consent.subject_identifier, )
        schedule_history = SubjectScheduleHistory.objects.get(
            schedule_name='a_tb1_6_months_schedule1',
            onschedule_model='flourish_caregiver.onschedulecohortatb6months',
            subject_identifier=self.consent.subject_identifier
        )
        self.assertIsNotNone(schedule_history.offschedule_datetime)

    def test_flourish_crfs(self):
        tb_crf = mommy.make_recipe('flourish_caregiver.tbroutinehealthscreenv2',
                                   maternal_visit=self.enrol_visit, )
        tb_crf.save()

    def test_tb_consent_on_flourish_crfs(self):
        mommy.make_recipe(
            'flourish_caregiver.tbinformedconsent',
            subject_identifier=self.consent.subject_identifier,
            consent_datetime=get_utcnow()
        )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.consent.subject_identifier, )

        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_2_months_schedule1').count(), 1)

        tb_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.consent.subject_identifier,
                visit_code='2100T'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe('flourish_caregiver.tbroutinehealthscreenv2',
                          maternal_visit=tb_visit, )

        mommy.make_recipe('flourish_caregiver.tbroutinehealthscreenv2',
                          maternal_visit=self.enrol_visit, )

    def prepare_off_study_2_months_visit(self):
        mommy.make_recipe(
            'flourish_caregiver.tbinformedconsent',
            subject_identifier=self.consent.subject_identifier,
            consent_datetime=get_utcnow()
        )
        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_2_months_schedule1').count(), 0)

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

        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='a_tb1_2_months_schedule1').count(), 1)

        tb_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.consent.subject_identifier,
                visit_code='2100T'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.tbvisitscreeningwomen',
            subject_identifier=self.consent.subject_identifier,
            visit_code='2100T').entry_status, REQUIRED)

        mommy.make_recipe('flourish_caregiver.tbvisitscreeningwomen',
                          have_cough=NO,
                          maternal_visit=tb_visit)
