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

        self.sh = SubjectHelperMixin()

        subject_identifier = self.sh.enroll_prior_participant(
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

    def test_post_referral_1000M_unscheduled_req(self):
        """ Assert post referral crf is required for pregnant ANC participant's
            referred at enrollment visit, and seen for unscheduled visit 7days
            after referral.
        """
        subject_identifier = self.sh.create_antenatal_enrollment(version='3')
        appt_1000M = Appointment.objects.get(visit_code='1000M',
                                             subject_identifier=subject_identifier)

        visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=appt_1000M,
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        phq_referral = mommy.make_recipe(
            'flourish_caregiver.caregiverphqreferral',
            report_datetime=get_utcnow(),
            maternal_visit=visit,
            referred_to='psychiatrist')

        appt_unscheduled = self.sh.create_unscheduled_appointment(
            base_appointment=appt_1000M)
        appt_unscheduled.appt_datetime = phq_referral.report_datetime + relativedelta(days=7)
        appt_unscheduled.save()

        unscheduled_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=appt_unscheduled,
            schedule_name=visit.schedule_name,
            visit_schedule_name=visit.visit_schedule_name,
            report_datetime=appt_unscheduled.appt_datetime)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqpostreferral',
                subject_identifier=subject_identifier,
                visit_code='1000M',
                visit_code_sequence=1).entry_status, REQUIRED)

        unscheduled_visit.report_datetime = phq_referral.report_datetime + relativedelta(days=6)
        unscheduled_visit.save()

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqpostreferral',
                subject_identifier=subject_identifier,
                visit_code='1000M',
                visit_code_sequence=1).entry_status, NOT_REQUIRED)

    def test_post_referral_required_anc_pos(self):
        """ Assert post referral crf is required for positive ANC participant's
            referred at enrollment, on the delivery and/or quarterly visits.
        """
        subject_identifier = self.sh.create_antenatal_enrollment(version='3')
        appt_1000M = Appointment.objects.get(visit_code='1000M',
                                             subject_identifier=subject_identifier)

        visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=appt_1000M,
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.caregiverphqreferral',
            report_datetime=get_utcnow(),
            maternal_visit=visit,
            referred_to='psychiatrist')

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=subject_identifier)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqpostreferral',
                subject_identifier=subject_identifier,
                visit_code='2000D', ).entry_status, REQUIRED)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                subject_identifier=subject_identifier,
                visit_code='2001M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqpostreferral',
                subject_identifier=subject_identifier,
                visit_code='2001M', ).entry_status, REQUIRED)
