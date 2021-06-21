import pytz
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NOT_APPLICABLE
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from edc_visit_schedule.models import SubjectScheduleHistory
from edc_appointment.models import Appointment
from ..models import OnScheduleCohortAAntenatal
from ..models import OnScheduleCohortAEnrollment, OnScheduleCohortABirth
from ..models import OnScheduleCohortAQuarterly, OnScheduleCohortAFU
from ..models import OnScheduleCohortBEnrollment, OnScheduleCohortBQuarterly
from ..models import OnScheduleCohortCEnrollment, OnScheduleCohortCQuarterly
from ..models import OnScheduleCohortASec, OnScheduleCohortBSec, OnScheduleCohortCSec
from ..models import OnScheduleCohortBFU, OnScheduleCohortCFU
from ..subject_helper_mixin import SubjectHelperMixin


@tag('vs')
class TestVisitScheduleSetup(TestCase):

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
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

    @tag('vs9')
    def test_cohort_a_onschedule_antenatal_valid(self):
        """Assert that a pregnant woman is put on cohort a schedule.
        """

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

        self.assertEqual(OnScheduleCohortAAntenatal.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_antenatal1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_quarterly1_schedule1').count(), 1)

    def test_cohort_a_onschedule_antenatal_and_onsec_valid(self):
        """Assert that a pregnant woman is put on cohort a schedule.
        """

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

        self.assertEqual(OnScheduleCohortAAntenatal.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_antenatal1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_quarterly1_schedule1').count(), 1)

        mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=2, months=5),
            **self.child_dataset_options)

        ccc2 = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=(get_utcnow() - relativedelta(years=2, months=5)).date(),)

        self.assertEqual(OnScheduleCohortAEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_quarterly2_schedule1').count(), 1)

        self.assertEqual(ccc2.caregiver_visit_count, 2)

    # def test_cohort_a_onschedule_birth_valid(self):
    #
        # screening_preg = mommy.make_recipe(
            # 'flourish_caregiver.screeningpregwomen',)
            #
        # subject_consent = mommy.make_recipe(
            # 'flourish_caregiver.subjectconsent',
            # screening_identifier=screening_preg.screening_identifier,
            # subject_identifier=self.subject_identifier,
            # breastfeed_intent=YES,
            # **self.options)
            #
        # mommy.make_recipe(
            # 'flourish_caregiver.antenatalenrollment',
            # subject_identifier=subject_consent.subject_identifier,)
            #
        # mommy.make_recipe(
            # 'flourish_caregiver.maternaldelivery',
            # subject_identifier=subject_consent.subject_identifier,)
            #
        # self.assertEqual(OnScheduleCohortABirth.objects.filter(
            # subject_identifier=subject_consent.subject_identifier,
            # schedule_name='a_birth1_schedule1').count(), 1)

    def test_cohort_a_onschedule_consent_valid(self):
        """Assert that a 2 year old participant's mother is put on cohort a schedule.
        """
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
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=(get_utcnow() - relativedelta(years=2, months=5)).date(),)

        self.assertEqual(OnScheduleCohortAEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_quarterly1_schedule1').count(), 1)

        # self.assertEqual(OnScheduleCohortAFU.objects.filter(
            # subject_identifier=subject_consent.subject_identifier,
            # schedule_name='a_fu1_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 0)

    def test_cohort_a_onschedule_sec_valid(self):
        """Assert that a 2 year old participant's mother is put on cohort a schedule.
        """
        self.subject_identifier = self.subject_identifier[:-1] + '1'

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            dob=get_utcnow() - relativedelta(years=2, months=5),
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
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=(get_utcnow() - relativedelta(years=2, months=5)).date(),)

        self.assertEqual(OnScheduleCohortAEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_quarterly1_schedule1').count(), 1)

        # self.assertEqual(OnScheduleCohortAFU.objects.filter(
            # subject_identifier=subject_consent.subject_identifier,
            # schedule_name='a_fu1_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 0)

    @tag('vs2')
    def test_cohort_b_onschedule_valid(self):
        """Assert that a 5 year old participant's mother who is on efv regimen from Mpepu study
         is put on cohort b schedule.
        """

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
            dob=get_utcnow() - relativedelta(years=5, months=2),
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
            schedule_name='b_quarterly1_schedule1').count(), 1)

        # self.assertEqual(OnScheduleCohortBFU.objects.filter(
            # subject_identifier=subject_identifier,
            # schedule_name='b_fu1_schedule1').count(), 1)
            #
        # self.assertEqual(Appointment.objects.get(
            # subject_identifier=subject_identifier,
            # schedule_name='b_fu1_schedule1',
            # visit_code='3000M').appt_datetime.date(), (django_apps.get_app_config(
                # 'edc_protocol').study_open_datetime + relativedelta(years=3)).date())

        self.assertGreater(Appointment.objects.filter(
            subject_identifier=subject_identifier).count(), 15)

    def test_cohort_b_onschedule_sec(self):
        """Assert that a 5 year old participant's mother who is on efv regimen is NOT put on
         cohort b schedule.
        """

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
            subject_identifier=self.subject_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=(get_utcnow() - relativedelta(years=5, months=2)).date(),)

        self.assertEqual(OnScheduleCohortBSec.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_sec1_schedule1').count(), 1)

        self.assertGreater(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_sec1_schedule1').count(), 15)

    def test_cohort_b_assent_onschedule_valid(self):
        """Assert that a 7 year old participant's mother who is HIV- from Mpepu study
         is put on cohort b schedule after assent.
        """

        self.subject_identifier = self.subject_identifier[:-1] + '3'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['mom_hivstatus'] = 'HIV uninfected'
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
            schedule_name='b_quarterly1_schedule1').count(), 1)

        # self.assertEqual(OnScheduleCohortBFU.objects.filter(
            # subject_identifier=subject_identifier,
            # schedule_name='b_fu1_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_identifier).count(), 0)

    def test_cohort_c_onschedule_valid(self):
        """Assert that a 10 year old participant's mother who is on the PI regimen from
         Mpepu study is put on cohort c.
        """
        self.subject_identifier = self.subject_identifier[:-1] + '4'

        self.maternal_dataset_options['protocol'] = 'Tshipidi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=10,
                                                                                months=2)
        self.maternal_dataset_options['preg_pi'] = 1

        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'
        self.options['subject_identifier'] = self.subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            dob=get_utcnow() - relativedelta(years=10, months=2),
            ** self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'])

        self.assertEqual(OnScheduleCohortCEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='c_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortCQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='c_quarterly1_schedule1').count(), 1)

        # self.assertEqual(OnScheduleCohortCFU.objects.filter(
            # subject_identifier=subject_identifier,
            # schedule_name='c_fu1_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_identifier).count(), 0)

    @tag('vs1')
    def test_cohort_c_sec_onschedule_valid(self):
        """Assert that a 10 year old participant's mother who is on the PI regimen from
         Mashi study is put on cohort c secondary aims.
        """
        self.subject_identifier = self.subject_identifier[:-1] + '4'

        self.maternal_dataset_options['protocol'] = 'Mashi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=16,
                                                                                months=4)
        self.maternal_dataset_options['preg_pi'] = 1

        self.child_dataset_options['infant_hiv_exposed'] = 'exposed'
        self.options['subject_identifier'] = self.subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            dob=get_utcnow() - relativedelta(years=16, months=4),
            ** self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'])

        self.assertEqual(OnScheduleCohortCSec.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='c_sec1_schedule1').count(), 1)

        self.assertGreater(Appointment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='c_sec1_schedule1').count(), 15)

    def test_cohort_b_twins_onschedule_valid(self):
        """Assert that a 9 year old twin participants' mother from  Mpepu study is put on
         cohort c with only one visit schedule.
        """
        self.subject_identifier = self.subject_identifier[:-1] + '9'
        self.study_maternal_identifier = '981231'
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

        # self.assertEqual(OnScheduleCohortBFU.objects.filter(
            # subject_identifier=subject_consent.subject_identifier,
            # schedule_name='b_fu1_schedule1').count(), 1)
            #
        # self.assertEqual(OnScheduleCohortBFU.objects.filter(
            # subject_identifier=subject_consent.subject_identifier,
            # schedule_name='b_fu2_schedule1').count(), 0)
            #
        # self.assertEqual(OnScheduleCohortBFU.objects.filter(
            # subject_identifier=subject_consent.subject_identifier,
            # schedule_name='b_fu3_schedule1').count(), 0)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 0)

    def test_cohort_b_triplets_onschedule_valid(self):
        """Assert that a 7 year old triplet participants' mother from  Mpepu study is put on
         cohort c with only one visit schedule.
        """

        self.subject_identifier = self.subject_identifier[:-1] + '7'
        self.study_maternal_identifier = '981237'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=5,
                                                                                months=2)
        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
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

        # self.assertEqual(OnScheduleCohortBFU.objects.filter(
            # subject_identifier=subject_consent.subject_identifier,
            # schedule_name='b_fu1_schedule1').count(), 1)
            #
        # self.assertEqual(OnScheduleCohortBFU.objects.filter(
            # subject_identifier=subject_consent.subject_identifier,
            # schedule_name='b_fu2_schedule1').count(), 0)
            #
        # self.assertEqual(OnScheduleCohortBFU.objects.filter(
            # subject_identifier=subject_consent.subject_identifier,
            # schedule_name='b_fu3_schedule1').count(), 0)

    def test_cohort_b_multiple_onschedule_valid(self):
        """Assert that a 4 year old and 5 years participants' mother from  Mpepu study is put
         on two different visit schedules.
        """
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

        child_dataset1 = mommy.make_recipe(
            'flourish_child.childdataset',
            twin_triplet=0,
            dob=get_utcnow() - relativedelta(years=4, months=9),
            **self.child_dataset_options)

        self.child_dataset_options['study_child_identifier'] = '1235'
        child_dataset2 = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=5, months=9),
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
            study_child_identifier=child_dataset1.study_child_identifier,
            child_dob=(get_utcnow() - relativedelta(years=4, months=9)).date(),)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset2.study_child_identifier,
            child_dob=(get_utcnow() - relativedelta(years=5, months=9)).date(),)

        self.assertEqual(SubjectScheduleHistory.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            onschedule_datetime=child_consent.created).count(), 3)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)

        # self.assertEqual(OnScheduleCohortBFU.objects.filter(
            # subject_identifier=subject_consent.subject_identifier,
            # schedule_name='b_fu1_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol2_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly2_schedule1').count(), 1)

        # self.assertEqual(OnScheduleCohortBFU.objects.filter(
            # subject_identifier=subject_consent.subject_identifier,
            # schedule_name='b_fu2_schedule1').count(), 1)

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly2_schedule1').count(), 0)
