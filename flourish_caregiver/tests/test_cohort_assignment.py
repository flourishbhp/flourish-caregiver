from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
import pytz

from edc_visit_schedule.models import SubjectScheduleHistory

from ..models import OnScheduleCohortAAntenatal
from ..models import OnScheduleCohortAQuarterly
from ..models import OnScheduleCohortBEnrollment, OnScheduleCohortBQuarterly


@tag('ca')
class TestCohortAssignmentSetup(TestCase):

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

        self.child_dummy_consent_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')

    def year_3_age(self, year_3_years, year_3_months):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        child_dob = start_date_year_3 - relativedelta(years=year_3_years,
                                                      months=year_3_months)
        return child_dob

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

        child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=None,
            child_dob=None,
            first_name=None,
            last_name=None)

        self.assertEqual(child_consent.cohort, 'cohort_a')

        self.assertEqual(OnScheduleCohortAAntenatal.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_antenatal1_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='a_quarterly1_schedule1').count(), 0)

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

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=YES,
            **self.options)

        child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.child_dataset_options.get('study_child_identifier'),
            child_dob=maternal_dataset_obj.delivdt,)

        child_dummy_consent = self.child_dummy_consent_cls.objects.get(
            subject_identifier=child_consent.subject_identifier)

        self.assertEqual(child_consent.cohort, 'cohort_b')

        self.assertEqual(child_dummy_consent.cohort, 'cohort_b')

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

    def test_cohort_b_lt10(self):
        """  Assert that a participant with a child who is less than
            10 years old at beginning of year 3 goes into cohort b schedule.
        """

        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = self.year_3_age(10, 0)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=self.year_3_age(10, 0),
            **self.child_dataset_options)

        self.options = {
                'consent_datetime': get_utcnow(),
                'version': '1'}

        mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version='1',
            child_version='1')

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=maternal_dataset_obj.delivdt,)

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj.subject_identifier,
            first_name=caregiver_child_consent_obj.first_name,
            last_name=caregiver_child_consent_obj.last_name,
            dob=caregiver_child_consent_obj.child_dob,
            identity=caregiver_child_consent_obj.identity,
            confirm_identity=caregiver_child_consent_obj.identity,
            remain_in_study=YES,
            version=subject_consent.version)

        child_dummy_consent = self.child_dummy_consent_cls.objects.get(
            subject_identifier=caregiver_child_consent_obj.subject_identifier)

        self.assertEqual(caregiver_child_consent_obj.cohort, 'cohort_b')

        self.assertEqual(child_dummy_consent.cohort, 'cohort_b')

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 0)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 0)

