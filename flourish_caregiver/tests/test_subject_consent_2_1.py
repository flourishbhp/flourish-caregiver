from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NOT_APPLICABLE
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from edc_appointment.models import Appointment
from edc_visit_tracking.constants import SCHEDULED
from flourish_caregiver.models.caregiver_child_consent import CaregiverChildConsent

from ..models import OnScheduleCohortBSec, OnScheduleCohortBSecQuart


class TestSubjectReConsent2_1(TestCase):

    def year_3_age(self, year_3_years, year_3_months):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        child_dob = start_date_year_3 - relativedelta(years=year_3_years,
                                                      months=year_3_months)
        return child_dob

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
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=None,
            child_dob=None,
            first_name=None,
            last_name=None)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier,)

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=subject_consent.subject_identifier,)

        self.assertEqual(CaregiverChildConsent.objects.filter(
            subject_identifier__startswith=subject_consent.subject_identifier).count(), 1)

    def test_cohort_b_onschedule_sec(self):
        """Assert that a 5 year old participant's mother who is on efv regimen is NOT put on
         cohort b schedule.
        """

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=5, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '89721',
            'protocol': 'Mpepu'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '89721',
            'study_child_identifier': '1234'}

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

