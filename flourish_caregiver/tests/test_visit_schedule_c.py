from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
import pytz

from edc_appointment.models import Appointment
from edc_visit_schedule.models import SubjectScheduleHistory

from ..models import OnScheduleCohortCEnrollment, OnScheduleCohortCQuarterly
from ..models import OnScheduleCohortCSec
from ..subject_helper_mixin import SubjectHelperMixin


@tag('vsc')
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
            'study_child_identifier': '1234'}

    def year_3_age(self, year_3_years, year_3_months):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        child_dob = start_date_year_3 - relativedelta(years=year_3_years,
                                                      months=year_3_months)
        return child_dob

    @tag('vsc1')
    def test_cohort_c_onschedule_valid(self):
        """Assert that a 10 year old participant's mother who is on the PI regimen from
         Mpepu study is put on cohort c.
        """
        self.subject_identifier = self.subject_identifier[:-1] + '4'

        self.maternal_dataset_options['protocol'] = 'Tshipidi'
        self.maternal_dataset_options['delivdt'] = self.year_3_age(11, 1)
        self.maternal_dataset_options['preg_pi'] = 1

        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'
        self.options['subject_identifier'] = self.subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            dob=self.year_3_age(11, 1),
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
        self.maternal_dataset_options['delivdt'] = self.year_3_age(16, 1)
        self.maternal_dataset_options['preg_pi'] = 1

        self.child_dataset_options['infant_hiv_exposed'] = 'exposed'
        self.options['subject_identifier'] = self.subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            dob=self.year_3_age(16, 1),
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
