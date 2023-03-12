from datetime import date

from dateutil.relativedelta import relativedelta
from django.test import tag
from django.test.testcases import TestCase
from django.utils import timezone

from ..helper_classes.cohort import Cohort


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

    def enrollment_and_cohort_assignment(
            self, protocol=None, age_year=None, age_month=None,
            consent_datetime=None, dtg=None, efv=None, infant_hiv_exposed=None,
            mum_hiv_status=None):
        """Creat a 5.1 year old by year 3 participant's mother who is on
         efv regimen from Mpepu study is put on cohort b schedule.
        """
        age_year = age_year
        age_month = age_month
        infant_hiv_exposed=infant_hiv_exposed
        mum_hiv_status=mum_hiv_status
        protocol=protocol
        dtg=dtg
        efv=efv
        consent_datetime = consent_datetime or get_utcnow()
        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = protocol
        self.maternal_dataset_options['delivdt'] = self.year_3_age(age_year, age_month)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=efv,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=self.year_3_age(age_year, age_month),
            **self.child_dataset_options)

        self.options = {
            'consent_datetime': consent_datetime,
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
    
        return child_dummy_consent.subject_identifier

