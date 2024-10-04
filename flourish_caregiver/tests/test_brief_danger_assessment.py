from django.test import tag, TestCase
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import YES 
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from flourish_caregiver.subject_helper_mixin import SubjectHelperMixin


@tag('bda')
class TestBriefDangerAssessment(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_identifier = '12345678'
        self.study_maternal_identifier = '89721'

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=15, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Mpepu',
            'delivdt': self.year_3_age(5, 1)}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        self.child = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=self.year_3_age(5, 1),
            **self.child_dataset_options)

        self.sh = SubjectHelperMixin()

        subject_identifier = self.sh.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'])

        self.enrol_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def year_3_age(self, year_3_years, year_3_months):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        child_dob = start_date_year_3 - relativedelta(years=year_3_years,
                                                      months=year_3_months)
        return child_dob

    def test_brief_danger_assessment_required(self):
        self.hitsscreening = mommy.make_recipe(
            'flourish_caregiver.hitsscreening',
            maternal_visit=self.enrol_visit,
            in_relationship=YES,
            physical_hurt='5',
            insults='5',
            threaten='5',
            screem_curse='5',
        )
        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.briefdangerassessment',
            subject_identifier=self.enrol_visit.subject_identifier,
            visit_code='2000M').entry_status, REQUIRED)

    def test_brief_danger_assessment_not_required(self):
        self.hitsscreening = mommy.make_recipe(
            'flourish_caregiver.hitsscreening',
            maternal_visit=self.enrol_visit,
            in_relationship=YES,
            physical_hurt='1',
            insults='1',
            threaten='1',
            screem_curse='1',
        )
        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_caregiver.briefdangerassessment',
            subject_identifier=self.enrol_visit.subject_identifier,
            visit_code='2000M').entry_status, NOT_REQUIRED)
