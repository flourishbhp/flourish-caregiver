from dateutil.relativedelta import relativedelta
from django.test import tag
from django.test.testcases import TestCase
from model_mommy import mommy
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays

from ..helper_classes.cohort_assignment import CohortAssignment
from ..models import OnScheduleCohortAEnrollment, CaregiverChildConsent, OnScheduleCohortBEnrollment


@tag('cohort_assign')
class TestCohortAssignment(TestCase):

    def setUp(self):
        import_holidays()

        enrollment_data = {
            'child_dob': (get_utcnow() - relativedelta(years=4, months=6)).date(),
            'enrolment_dt': get_utcnow().date(),
            'child_hiv_exposure': 'exposed',
            'arv_regimen': '3-drug ART',
            'total_HEU': 20,
            'total_HUU': 10}

        self.helper_cls = CohortAssignment(**enrollment_data)

        self.subject_identifier = '12345678'
        study_maternal_identifier = '89721'

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'mom_pregarv_strat': 'blah',
            'study_maternal_identifier': study_maternal_identifier,
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': study_maternal_identifier,
            'study_child_identifier': '1234'}

        self.maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=2, months=5),
            **self.child_dataset_options)

    def test_age_calculation(self):
        child_dob = (get_utcnow() - relativedelta(years=5, months=6)).date()
        self.helper_cls.child_dob = child_dob

        self.assertEquals(self.helper_cls.child_age, 5.5)

    def test_cohort_a_heu(self):
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_a', )

    def test_cohort_a_huu(self):
        self.helper_cls.child_hiv_exposure = 'unexposed'
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_a', )

    def test_cohort_a_heu_limit(self):
        self.helper_cls.total_HEU = 450
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_a_sec', )

    def test_cohort_a_huu_limit(self):
        self.helper_cls.child_hiv_exposure = 'unexposed'
        self.helper_cls.total_HUU = 325
        self.assertIsNot(self.helper_cls.cohort_variable, 'cohort_a', )
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_a_sec', )

    def test_cohort_b_heu(self):
        child_dob = (get_utcnow() - relativedelta(years=9, months=4)).date()
        self.helper_cls.child_dob = child_dob
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_b', )

    def test_cohort_b_huu(self):
        child_dob = (get_utcnow() - relativedelta(years=5, months=1)).date()
        self.helper_cls.child_dob = child_dob
        self.helper_cls.child_hiv_exposure = 'unexposed'
        self.helper_cls.arv_regimen = None
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_b', )

    def test_cohort_b_heu_limit(self):
        child_dob = (get_utcnow() - relativedelta(years=9, months=4)).date()
        self.helper_cls.child_dob = child_dob
        self.helper_cls.total_HEU = 200
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_b_sec', )

    def test_cohort_b_huu_limit(self):
        child_dob = (get_utcnow() - relativedelta(years=8, days=2)).date()
        self.helper_cls.child_dob = child_dob
        self.helper_cls.child_hiv_exposure = 'Unexposed'
        self.helper_cls.arv_regimen = None
        self.helper_cls.total_HUU = 325
        self.assertIsNot(self.helper_cls.cohort_variable, 'cohort_b', )
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_b_sec', )

    def test_cohort_c_heu(self):
        child_dob = (get_utcnow() - relativedelta(years=10, months=1)).date()
        self.helper_cls.child_dob = child_dob
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_c', )

    def test_cohort_c_huu(self):
        child_dob = (get_utcnow() - relativedelta(years=12)).date()
        self.helper_cls.child_dob = child_dob
        self.helper_cls.child_hiv_exposure = 'unexposed'
        self.helper_cls.arv_regimen = None
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_c', )

    def test_cohort_c_heu_limit(self):
        child_dob = (get_utcnow() - relativedelta(years=10, months=4)).date()
        self.helper_cls.child_dob = child_dob
        self.helper_cls.total_HEU = 100
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_c_sec', )

    def test_cohort_c_huu_limit(self):
        child_dob = (get_utcnow() - relativedelta(years=10, months=4)).date()
        self.helper_cls.child_dob = child_dob
        self.helper_cls.child_hiv_exposure = 'unexposed'
        self.helper_cls.arv_regimen = None
        self.helper_cls.total_HUU = 200
        self.assertIsNot(self.helper_cls.cohort_variable, 'cohort_c', )
        self.assertEqual(self.helper_cls.cohort_variable, 'cohort_c_sec', )

    def test_cohort_a_dataset_valid(self):
        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=self.maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=self.maternal_dataset_obj.screening_identifier,
            subject_identifier=self.subject_identifier,
            breastfeed_intent=YES,
            **self.options)

        child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=(get_utcnow() - relativedelta(years=2, months=5)).date(),)

        mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled',
                subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(
            CaregiverChildConsent.objects.get(
                subject_identifier=child_consent.subject_identifier).cohort,
            'cohort_a', )

        self.assertEqual(OnScheduleCohortAEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_enrol1_schedule1').count(), 1)

    def test_cohort_b_dataset_valid(self):
        self.maternal_dataset_options.update(
            mom_pregarv_strat='3-drug ART',
            delivdt=get_utcnow() - relativedelta(years=5, months=5),
            study_maternal_identifier='112233', )

        self.child_dataset_options.update(
            study_maternal_identifier='112233',
            study_child_identifier='332123', )

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier='12345',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=5, months=5),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=(get_utcnow() - relativedelta(years=2, months=5)).date(),)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(
            CaregiverChildConsent.objects.get(
                subject_identifier=child_consent.subject_identifier).cohort,
            'cohort_b', )

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

    def test_sec_cohort_dataset_valid(self):
        self.maternal_dataset_options.update(
            mom_pregarv_strat='blah',
            delivdt=get_utcnow() - relativedelta(years=5, months=5),
            study_maternal_identifier='112233', )

        self.child_dataset_options.update(
            study_maternal_identifier='112233',
            study_child_identifier='332123', )

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier='12345',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=5, months=5),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=(get_utcnow() - relativedelta(years=2, months=5)).date(),)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(
            CaregiverChildConsent.objects.get(
                subject_identifier=child_consent.subject_identifier).cohort,
            'cohort_b_sec', )
