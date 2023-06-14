import pytz
from django.apps import apps as django_apps
from django.test import TestCase, tag
from unittest import skip
from edc_base import get_utcnow
from edc_facility.import_holidays import import_holidays

from flourish_caregiver.helper_classes.sequential_subject_helper import \
    SequentialSubjectHelper
from flourish_caregiver.models import (OnScheduleCohortAEnrollment, OnScheduleCohortBEnrollment,
                                       OnScheduleCohortCSec, OnScheduleCohortAQuarterly,
                                       OnScheduleCohortBSecQuart, OnScheduleCohortBQuarterly, OnScheduleCohortCQuarterly)
from model_mommy import mommy
from dateutil.relativedelta import relativedelta
from edc_visit_schedule import site_visit_schedules
from flourish_caregiver.helper_classes.sequential_cohort_enrollment import SequentialCohortEnrollment
from edc_registration.models import RegisteredSubject


@tag('sq')
class TestSequentialEnrollmentCohort(TestCase):
    databases = '__all__'
    utc = pytz.UTC

    child_cohort_a_quartely_model = 'flourish_child.onschedulechildcohortaquarterly'
    child_cohort_b_quartely_model = 'flourish_child.onschedulechildcohortbquarterly'
    child_cohort_b_sec_quartely_model = 'flourish_child.onschedulechildcohortbsecquart'
    child_cohort_c_quartely_model = 'flourish_child.onschedulechildcohortcquarterly'
    child_cohort_c_sec_quartely_model = 'flourish_child.onschedulechildcohortcsecquart'

    def setUp(self):
        import_holidays()
        self.subject_identifier = 'B142-040990120-3'
        self.study_maternal_identifier = '89721'
        self.study_child_identifier = '89721'
        self.child_subject_identifier = 'B142-040990120-3-10'
        self.child_dob = (
            get_utcnow() - relativedelta(years=6)).date()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
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

        self.sequential_helper = SequentialSubjectHelper(
            child_dataset_options=self.child_dataset_options,
            maternal_dataset_options=self.maternal_dataset_options
        )

    @property
    def child_cohort_a_quartely_cls(self):
        return django_apps.get_model(self.child_cohort_a_quartely_model)

    @property
    def child_cohort_b_quartely_cls(self):
        return django_apps.get_model(self.child_cohort_b_quartely_model)

    @property
    def child_cohort_b_sec_quartely_cls(self):
        return django_apps.get_model(self.child_cohort_b_sec_quartely_model)

    @property
    def child_cohort_c_quartely_cls(self):
        return django_apps.get_model(self.child_cohort_c_quartely_model)

    @property
    def child_cohort_c_sec_quartely_cls(self):
        return django_apps.get_model(self.child_cohort_c_sec_quartely_model)

    @skip('zlz')
    def test_cohort_a_onschedule(self):
        subject_identifier = self.sequential_helper.get_cohort_a_subj()
        self.assertNotEqual(subject_identifier, None)
        self.assertEqual(OnScheduleCohortAEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='a_enrol1_schedule1').count(), 1)

    @skip('zlz')
    def test_cohort_b_onschedule(self):
        subject_identifier = self.sequential_helper.get_cohort_b_subj()
        self.assertNotEqual(subject_identifier, None)
        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

    @skip('zlz')
    def test_cohort_c_onschedule(self):
        subject_identifier = self.sequential_helper.get_cohort_c_subj()
        self.assertNotEqual(subject_identifier, None)
        self.assertEqual(OnScheduleCohortCSec.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='c_sec1_schedule1').count(), 1)

    @tag('caregiver_sq')
    def test_caregiver_cohort_a_to_cohort_b(self):

        self.child_dataset = mommy.make_recipe('flourish_child.childdataset',
                                               dob=self.child_dob,
                                               infant_hiv_exposed='Unexposed',
                                               study_maternal_identifier=self.study_maternal_identifier,
                                               study_child_identifier=self.study_child_identifier)

        self.subject_consent = mommy.make_recipe('flourish_caregiver.subjectconsent',
                                                 subject_identifier=self.subject_identifier,)

        self.caregiver_child_consent = mommy.make_recipe('flourish_caregiver.caregiverchildconsent',
                                                         subject_identifier=self.child_subject_identifier,
                                                         subject_consent=self.subject_consent,
                                                         study_child_identifier=self.study_child_identifier,
                                                         child_dob=self.child_dob)

        mommy.make_recipe('flourish_caregiver.maternaldataset',
                          subject_identifier=self.subject_identifier,
                          study_maternal_identifier=self.study_maternal_identifier,
                          protocol='Tshipidi')
        mommy.make_recipe('flourish_child.childdummysubjectconsent',
                          subject_identifier=self.child_subject_identifier,
                          dob=self.caregiver_child_consent.child_dob)

        _, caregiver_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model='flourish_caregiver.onschedulecohortaquarterly',
            name='a_quarterly1_schedule1'
        )

        _, child_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=self.child_cohort_a_quartely_model,
            name='child_a_quart_schedule1'
        )

        caregiver_schedule.put_on_schedule(
            subject_identifier=self.subject_identifier,
            onschedule_datetime=get_utcnow(),
            schedule_name='a_quarterly1_schedule1')

        child_schedule.put_on_schedule(
            subject_identifier=self.child_subject_identifier,
            onschedule_datetime=get_utcnow(),
            schedule_name='child_a_quart_schedule1')

        sq_erollment = SequentialCohortEnrollment(
            child_subject_identifier=self.child_subject_identifier)

        sq_erollment.put_caregiver_onschedule()

        self.assertTrue(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=self.subject_identifier).exists())

    @tag('caregiver_sq')
    def test_caregiver_cohort_b_to_cohort_c(self):

        self.child_dob = (
            get_utcnow() - relativedelta(years=11)).date()

        self.child_dataset = mommy.make_recipe('flourish_child.childdataset',
                                               dob=self.child_dob,
                                               infant_hiv_exposed='Unexposed',
                                               study_maternal_identifier=self.study_maternal_identifier,
                                               study_child_identifier=self.study_child_identifier)

        self.subject_consent = mommy.make_recipe('flourish_caregiver.subjectconsent',
                                                 subject_identifier=self.subject_identifier,)

        self.caregiver_child_consent = mommy.make_recipe('flourish_caregiver.caregiverchildconsent',
                                                         subject_identifier=self.child_subject_identifier,
                                                         subject_consent=self.subject_consent,
                                                         study_child_identifier=self.study_child_identifier,
                                                         child_dob=self.child_dob)

        mommy.make_recipe('flourish_caregiver.maternaldataset',
                          subject_identifier=self.subject_identifier,
                          study_maternal_identifier=self.study_maternal_identifier,
                          protocol='Tshipidi')
        mommy.make_recipe('flourish_child.childdummysubjectconsent',
                          subject_identifier=self.child_subject_identifier,
                          dob=self.caregiver_child_consent.child_dob)

        _, caregiver_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model='flourish_caregiver.onschedulecohortbquarterly',
            name='b_quarterly1_schedule1'
        )

        _, child_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=self.child_cohort_b_quartely_model,
            name='child_b_quart_schedule1'
        )

        caregiver_schedule.put_on_schedule(
            subject_identifier=self.subject_identifier,
            onschedule_datetime=get_utcnow(),
            schedule_name='b_quarterly1_schedule1')

        child_schedule.put_on_schedule(
            subject_identifier=self.child_subject_identifier,
            onschedule_datetime=get_utcnow(),
            schedule_name='child_b_quart_schedule1')

        sq_erollment = SequentialCohortEnrollment(
            child_subject_identifier=self.child_subject_identifier)

        sq_erollment.put_caregiver_onschedule()

        self.assertTrue(OnScheduleCohortCQuarterly.objects.filter(
            subject_identifier=self.subject_identifier).exists())

    @tag('child_sq')
    def test_child_cohort_a_to_cohort_b(self):
        self.child_dataset = mommy.make_recipe('flourish_child.childdataset',
                                               dob=self.child_dob,
                                               study_maternal_identifier=self.study_maternal_identifier,
                                               study_child_identifier=self.study_child_identifier)

        self.subject_consent = mommy.make_recipe('flourish_caregiver.subjectconsent',
                                                 subject_identifier=self.subject_identifier,)

        self.caregiver_child_consent = mommy.make_recipe('flourish_caregiver.caregiverchildconsent',
                                                         subject_identifier=self.child_subject_identifier,
                                                         subject_consent=self.subject_consent,
                                                         study_child_identifier=self.study_child_identifier,
                                                         child_dob=self.child_dob)

        mommy.make_recipe('flourish_caregiver.maternaldataset',
                          subject_identifier=self.subject_identifier,
                          study_maternal_identifier=self.study_maternal_identifier,
                          protocol='Mpepu')
        mommy.make_recipe('flourish_child.childdummysubjectconsent',
                          subject_identifier=self.child_subject_identifier,
                          dob=self.caregiver_child_consent.child_dob)

        _, child_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=self.child_cohort_a_quartely_model,
            name='child_a_quart_schedule1'
        )

        child_schedule.put_on_schedule(
            subject_identifier=self.child_subject_identifier,
            onschedule_datetime=get_utcnow(),
            schedule_name='child_a_quart_schedule1')

        sq_erollment = SequentialCohortEnrollment(
            child_subject_identifier=self.child_subject_identifier)

        sq_erollment.put_child_onschedule()

        self.assertTrue(self.child_cohort_b_sec_quartely_cls.objects.filter(
            subject_identifier=self.child_subject_identifier).exists())

    @tag('child_sq')
    def test_child_cohort_b_to_cohort_c(self):
        self.child_dob = (
            get_utcnow() - relativedelta(years=11)).date()
        self.child_dataset = mommy.make_recipe('flourish_child.childdataset',
                                               dob=self.child_dob,
                                               study_maternal_identifier=self.study_maternal_identifier,
                                               study_child_identifier=self.study_child_identifier,
                                               infant_hiv_exposed='Unexposed')

        self.subject_consent = mommy.make_recipe('flourish_caregiver.subjectconsent',
                                                 subject_identifier=self.subject_identifier,)

        self.caregiver_child_consent = mommy.make_recipe('flourish_caregiver.caregiverchildconsent',
                                                         subject_identifier=self.child_subject_identifier,
                                                         subject_consent=self.subject_consent,
                                                         study_child_identifier=self.study_child_identifier,
                                                         child_dob=self.child_dob)

        mommy.make_recipe('flourish_caregiver.maternaldataset',
                          subject_identifier=self.subject_identifier,
                          study_maternal_identifier=self.study_maternal_identifier,
                          protocol='Tshipidi')

        mommy.make_recipe('flourish_child.childdummysubjectconsent',
                          subject_identifier=self.child_subject_identifier,
                          dob=self.caregiver_child_consent.child_dob)

        _, child_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=self.child_cohort_b_quartely_model,
            name='child_b_quart_schedule1'
        )

        child_schedule.put_on_schedule(
            subject_identifier=self.child_subject_identifier,
            onschedule_datetime=get_utcnow(),
            schedule_name='child_b_quart_schedule1')

        sq_erollment = SequentialCohortEnrollment(
            child_subject_identifier=self.child_subject_identifier)

        sq_erollment.put_child_onschedule()

        self.assertTrue(self.child_cohort_c_quartely_cls.objects.filter(
            subject_identifier=self.child_subject_identifier).exists())
