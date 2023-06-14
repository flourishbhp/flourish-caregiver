from datetime import date

from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
import pytz

from edc_appointment.models import Appointment
from edc_visit_schedule.models import SubjectScheduleHistory
from edc_visit_tracking.constants import SCHEDULED

from ..models import OnScheduleCohortBEnrollment, OnScheduleCohortBQuarterly
from ..models import OnScheduleCohortBSec, OnScheduleCohortBSecQuart
from ..subject_helper_mixin import SubjectHelperMixin


@tag('vsb')
class TestVisitScheduleSetupB(TestCase):

    databases = '__all__'
    utc = pytz.UTC

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

    def year_3_age(self, year_3_years, year_3_months):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        child_dob = start_date_year_3 - relativedelta(years=year_3_years,
                                                      months=year_3_months)
        return child_dob

    def test_cohort_b_onschedule_invalid1(self):
        """Assert that a 5.1 year old by year 3 participant's mother who is on
         efv regimen from BCPP study is not put on cohort b schedule.
        """

        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = 'BCPP'
        self.maternal_dataset_options['delivdt'] = date(2011, 7, 13)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=date(2011, 7, 13),
            **self.child_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'])

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

    def test_cohort_b_onschedule_valid(self):
        """Assert that a 5.1 year old by year 3 participant's mother who is on
         efv regimen from Mpepu study is put on cohort b schedule.
        """

        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = self.year_3_age(5, 1)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=self.year_3_age(5, 1),
            **self.child_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'])

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_identifier).count(), 9)

    def test_cohort_b_assent_invalid(self):
        """Assert that a 6 year old whose birthday is within the enrollment month does not get
         served the assent form.
        """

        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=6,
                                                                                months=11,
                                                                                days=25)
        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=6, months=11, days=25),
            **self.child_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'])

        child_assent_model = django_apps.get_model('flourish_child.childassent')

        self.assertEqual(child_assent_model.objects.filter(
            subject_identifier__startswith=subject_identifier).count(), 0)

    def test_cohort_b_lt10(self):
        """Assert that a participant with a child who is lt 10 years old at beginning
         of year 3 goes into cohort b schedule.
        """

        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = self.year_3_age(9, 5)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=self.year_3_age(9, 5),
            **self.child_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'])

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)

    def test_cohort_b_onschedule_sec(self):
        """Assert that a 5 year old participant's mother who is on efv regimen is NOT put on
         cohort b schedule.
        """

        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = self.year_3_age(5, 5)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=0,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            dob=self.year_3_age(5, 5),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=self.year_3_age(5, 5),)

        mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled',
                subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(OnScheduleCohortBSec.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_sec1_schedule1').count(), 1)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_sec1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBSecQuart.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_sec_quart1_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleCohortBSecQuart.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_sec_quart1_schedule1').count(), 1)

    def test_cohort_b_assent_onschedule_valid(self):
        """Assert that a 7 year old participant's mother who is HIV- from Mpepu study
         is put on cohort b schedule after assent.
        """

        self.subject_identifier = self.subject_identifier[:-1] + '3'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['mom_hivstatus'] = 'HIV-uninfected'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=7,
                                                                                months=2)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=7, months=2),
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'])

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_identifier).count(), 0)

    def test_cohort_b_twins_onschedule_valid(self):
        """Assert that an 8 year old twin participants' mother from  Mpepu study is put on
         cohort c with only one visit schedule.
        """
        self.subject_identifier = self.subject_identifier[:-1] + '9'
        self.study_maternal_identifier = '981231'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=8,
                                                                                months=2)
        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            twin_triplet=1,
            preg_efv=1,
            **self.maternal_dataset_options)

        cd1 = mommy.make_recipe(
            'flourish_child.childdataset',
            twin_triplet=1,
            dob=get_utcnow() - relativedelta(years=8, months=2),
            **self.child_dataset_options)

        self.child_dataset_options['study_child_identifier'] = '1235'

        cd2 = mommy.make_recipe(
            'flourish_child.childdataset',
            twin_triplet=1,
            dob=get_utcnow() - relativedelta(years=8, months=2),
            ** self.child_dataset_options)

        mommy.make_recipe(
                'flourish_caregiver.flourishconsentversion',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                version='1',
                child_version='1')

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        child_consent1 = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=cd1.study_child_identifier,
            child_dob=(get_utcnow() - relativedelta(years=8, months=2)).date(),)

        mommy.make_recipe(
                'flourish_child.childassent',
                subject_identifier=child_consent1.subject_identifier,
                first_name=child_consent1.first_name,
                last_name=child_consent1.last_name,
                dob=child_consent1.child_dob,
                identity=child_consent1.identity,
                confirm_identity=child_consent1.identity,
                remain_in_study=YES,
                version=subject_consent.version)

        child_consent2 = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=cd2.study_child_identifier,
            identity='234513181',
            confirm_identity='234513181',
            child_dob=(get_utcnow() - relativedelta(years=8, months=2)).date(),)

        mommy.make_recipe(
                'flourish_child.childassent',
                subject_identifier=child_consent2.subject_identifier,
                first_name=child_consent2.first_name,
                last_name=child_consent2.last_name,
                dob=child_consent2.child_dob,
                identity=child_consent2.identity,
                confirm_identity=child_consent2.identity,
                remain_in_study=YES,
                version=subject_consent.version)

        mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled',
                subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol2_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol3_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly2_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly2_schedule1').count(), 0)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 0)

    def test_cohort_b_triplets_onschedule_valid(self):
        """Assert that a 5 year old triplet participants' mother from  Mpepu study is put on
         cohort c with only one visit schedule.
        """

        self.subject_identifier = self.subject_identifier[:-1] + '7'
        self.study_maternal_identifier = '981237'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=5,
                                                                                months=2)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            twin_triplet=1,
            preg_efv=1,
            **self.maternal_dataset_options)

        cd1 = mommy.make_recipe(
            'flourish_child.childdataset',
            twin_triplet=1,
            dob=get_utcnow() - relativedelta(years=5, months=2),
            **self.child_dataset_options)

        self.child_dataset_options['study_child_identifier'] = '1235'
        cd2 = mommy.make_recipe(
            'flourish_child.childdataset',
            twin_triplet=1,
            dob=get_utcnow() - relativedelta(years=5, months=2),
            ** self.child_dataset_options)

        self.child_dataset_options['study_child_identifier'] = '1236'
        cd3 = mommy.make_recipe(
            'flourish_child.childdataset',
            twin_triplet=1,
            dob=get_utcnow() - relativedelta(years=5, months=2),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=cd1.study_child_identifier,
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=cd2.study_child_identifier,
            identity='234513181',
            confirm_identity='234513181',
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=cd3.study_child_identifier,
            identity='234513182',
            confirm_identity='234513182',
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

        mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled',
                subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol2_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol3_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly2_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly3_schedule1').count(), 0)

    def test_cohort_b_multiple_onschedule_valid(self):
        """Assert that a 4 year old and 5 years participants' mother from  Mpepu study is put
         on two different visit schedules.
        """
        self.subject_identifier = self.subject_identifier[:-1] + '4'
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=5,
                                                                                months=1)

        mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            **self.maternal_dataset_options)

        self.maternal_dataset_options['study_maternal_identifier'] = self.study_maternal_identifier

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            **self.maternal_dataset_options)

        child_dataset1 = mommy.make_recipe(
            'flourish_child.childdataset',
            twin_triplet=0,
            dob=(get_utcnow() - relativedelta(years=5, months=1)).date(),
            **self.child_dataset_options)
        

        self.child_dataset_options['study_maternal_identifier'] = self.study_maternal_identifier
        self.child_dataset_options['study_child_identifier'] = '1235'
        child_dataset2 = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=(get_utcnow() - relativedelta(years=6, months=9)).date(),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset1.study_child_identifier,
            child_dob=(get_utcnow() - relativedelta(years=5, months=1)).date(),)

        prev_enrol = mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset2.study_child_identifier,
            child_dob=(get_utcnow() - relativedelta(years=6, months=9)).date(),)

        prev_enrol.save()

        self.assertEqual(SubjectScheduleHistory.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            onschedule_datetime__date=child_consent.created.date()).count(), 2)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_consent.subject_identifier,
                schedule_name='b_enrol1_schedule1'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)
