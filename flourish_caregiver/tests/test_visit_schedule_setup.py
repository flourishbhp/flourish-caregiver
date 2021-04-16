from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from edc_visit_schedule.models import SubjectScheduleHistory
from edc_appointment.models import Appointment

from ..models import OnScheduleCohortAEnrollment, OnScheduleCohortABirth
from ..models import OnScheduleCohortAQuarterly
from ..models import OnScheduleCohortBEnrollment, OnScheduleCohortBQuarterly
from ..models import OnScheduleCohortCEnrollment, OnScheduleCohortCQuarterly
from ..models import OnScheduleCohortCPool, OnScheduleSecB, OnScheduleSecC
from ..subject_helper_mixin import SubjectHelperMixin


@tag('vs')
class TestVisitScheduleSetup(TestCase):

    databases = '__all__'

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

    def test_cohort_a_onschedule_antenatal_valid(self):

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            subject_identifier=self.subject_identifier,
            breastfeed_intent=YES,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier,)

        self.assertEqual(OnScheduleCohortAEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_quarterly1_schedule1').count(), 1)

    def test_cohort_a_onschedule_birth_valid(self):

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            subject_identifier=self.subject_identifier,
            breastfeed_intent=YES,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier,)

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=subject_consent.subject_identifier,)

        self.assertEqual(OnScheduleCohortABirth.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_birth1_schedule1').count(), 1)

    def test_cohort_a_onschedule_consent_valid(self):
        self.subject_identifier = self.subject_identifier[:-1] + '1'

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            subject_identifier=self.subject_identifier,
            breastfeed_intent=YES,
            ** self.options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=2, months=5)).date(),)

        self.assertEqual(OnScheduleCohortAEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_quarterly1_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 0)

    def test_cohort_b_onschedule_valid(self):

        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=5,
                                                                                months=2)
        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            **self.child_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_identifier).count(), 0)

    def test_cohort_b_onschedule_invalid(self):

        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=5,
                                                                                months=2)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=0,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
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
            subject_identifier=self.subject_identifier,
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 0)

    def test_cohort_b_assent_onschedule_valid(self):

        self.subject_identifier = self.subject_identifier[:-1] + '3'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['mom_hivstatus'] = 'HIV uninfected'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=7,
                                                                                months=2)

        mommy.make_recipe(
            'flourish_child.childdataset',
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_identifier).count(), 0)

    def test_cohort_b_assent_onschedule_invalid(self):

        self.subject_identifier = self.subject_identifier[:-1] + '3'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['mom_hivstatus'] = 'HIV uninfected'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=7,
                                                                                months=2)
        self.options['subject_identifier'] = self.subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=7, months=2)).date(),)

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=self.subject_identifier + '-10',
            dob=get_utcnow() - relativedelta(years=7, months=2),
            identity=caregiver_child_consent_obj.identity,
            confirm_identity=caregiver_child_consent_obj.identity,
            remain_in_study=NO,
            version=subject_consent.version)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 0)

    def test_cohort_c_onschedule_valid(self):
        self.subject_identifier = self.subject_identifier[:-1] + '4'

        self.maternal_dataset_options['protocol'] = 'Mashi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=10,
                                                                                months=2)
        self.maternal_dataset_options['preg_pi'] = 1

        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'
        self.options['subject_identifier'] = self.subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier)

        self.assertEqual(OnScheduleCohortCEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='c_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortCQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='c_quarterly1_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_identifier).count(), 0)

    def test_cohort_b_twins_onschedule_valid(self):
        self.subject_identifier = self.subject_identifier[:-1] + '9'
        self.study_maternal_identifier = '981231'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=5,
                                                                                months=2)
        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        ccc = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            subject_identifier=subject_consent.subject_identifier + '-25',
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

        ccc2 = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            subject_identifier=subject_consent.subject_identifier + '-35',
            identity='234513181',
            confirm_identity='234513181',
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

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
        self.subject_identifier = self.subject_identifier[:-1] + '7'
        self.study_maternal_identifier = '981237'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=5,
                                                                                months=2)
        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
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
            subject_identifier=subject_consent.subject_identifier + '-36',
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            subject_identifier=subject_consent.subject_identifier + '-46',
            identity='234513181',
            confirm_identity='234513181',
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            subject_identifier=subject_consent.subject_identifier + '-56',
            identity='234513182',
            confirm_identity='234513182',
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

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
            schedule_name='b_quarterly1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly2_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly3_schedule1').count(), 0)

    @tag('vs1')
    def test_cohort_b_multiple_onschedule_valid(self):
        self.subject_identifier = self.subject_identifier[:-1] + '4'
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=4,
                                                                                months=9)
        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            subject_identifier=self.subject_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            subject_identifier=subject_consent.subject_identifier + '-10',
            child_dob=(get_utcnow() - relativedelta(years=4, months=9)).date(),)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            subject_identifier=subject_consent.subject_identifier + '-60',
            identity='234513181',
            confirm_identity='234513181',
            child_dob=(get_utcnow() - relativedelta(years=5, months=9)).date(),)

        self.assertEqual(SubjectScheduleHistory.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            onschedule_datetime=child_consent.created).count(), 1)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol2_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly2_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly2_schedule1').count(), 0)
