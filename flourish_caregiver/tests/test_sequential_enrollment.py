import pytz
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base import get_utcnow
from edc_facility.import_holidays import import_holidays

from flourish_caregiver.helper_classes.sequential_subject_helper import \
    SequentialSubjectHelper
from flourish_caregiver.models import OnScheduleCohortAEnrollment, \
    OnScheduleCohortBEnrollment, OnScheduleCohortCSec


class TestSequentialEnrollmentCohort(TestCase):
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

    @tag('zlz')
    def test_cohort_a_onschedule(self):
        subject_identifier = self.sequential_helper.get_cohort_a_subj()
        self.assertNotEqual(subject_identifier, None)
        self.assertEqual(OnScheduleCohortAEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='a_enrol1_schedule1').count(), 1)

    @tag('zlz')
    def test_cohort_b_onschedule(self):
        subject_identifier = self.sequential_helper.get_cohort_b_subj()
        self.assertNotEqual(subject_identifier, None)
        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

    @tag('zlz')
    def test_cohort_c_onschedule(self):
        subject_identifier = self.sequential_helper.get_cohort_c_subj()
        self.assertNotEqual(subject_identifier, None)
        self.assertEqual(OnScheduleCohortCSec.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='c_sec1_schedule1').count(), 1)
