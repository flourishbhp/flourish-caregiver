from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy
import pytz

from edc_appointment.models import Appointment
from edc_visit_schedule.models import SubjectScheduleHistory
from edc_visit_tracking.constants import SCHEDULED

from ..models import MaternalVisit
from ..subject_helper_mixin import SubjectHelperMixin


@tag('reff')
class TestReferralRuleGroups(TestCase):

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

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=self.year_3_age(5, 1),
            **self.child_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'])

        mommy.make_recipe(
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

    def test_phq9_referral_required(self):

        visit = MaternalVisit.objects.get(visit_code='2000M')
        mommy.make_recipe('flourish_caregiver.caregiverphqdeprscreening',
                          maternal_visit=visit)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqreferral',
                subject_identifier=visit.subject_identifier,
                visit_code='2000M').entry_status, REQUIRED)

    def test_phq9_referral_fu_required(self):

        visit = MaternalVisit.objects.get(visit_code='2000M')
        mommy.make_recipe('flourish_caregiver.caregiverphqdeprscreening',
                          maternal_visit=visit)

        mommy.make_recipe('flourish_caregiver.caregiverphqreferral',
                          maternal_visit=visit,
                          referred_to='receiving_emotional_care')

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqreferralfu',
                subject_identifier=visit.subject_identifier,
                visit_code='2000M').entry_status, REQUIRED)

    def test_phq9_post_referral_required(self):

        visit = MaternalVisit.objects.get(visit_code='2000M')
        mommy.make_recipe('flourish_caregiver.caregiverphqdeprscreening',
                          maternal_visit=visit)

        mommy.make_recipe('flourish_caregiver.caregiverphqreferral',
                          maternal_visit=visit,
                          referred_to='psychiatrist')

        quart_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2001M',
                subject_identifier=visit.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqpostreferral',
                subject_identifier=quart_visit.subject_identifier,
                visit_code='2001M').entry_status, REQUIRED)
