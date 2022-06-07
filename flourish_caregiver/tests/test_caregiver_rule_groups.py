from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NEG, POS
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from edc_appointment.models import Appointment
from edc_visit_schedule.subject_schedule import SubjectSchedule
from edc_visit_tracking.constants import SCHEDULED

from ..models import MaternalVisit
from ..subject_helper_mixin import SubjectHelperMixin


@tag('rg')
class TestRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'breastfeed_intent': YES,
            'version': '1'}

        self.screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen')

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=self.screening_preg.screening_identifier,
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            child_dob=None,
            first_name=None,
            last_name=None,)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=self.subject_consent.subject_identifier)

        self.subject_identifier = self.subject_consent.subject_identifier

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(visit_code='1000M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    @tag('bbh')
    def test_hiv_viralload_cd4_not_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivviralloadandcd4',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    @tag('sub')
    def test_substanceuse_prior_to_preg_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.substanceusepriorpregnancy',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('rg1')
    def test_hiv_test_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivrapidtestcounseling',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    def test_arvsprepregnancy_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.arvsprepregnancy',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_arvsduringpregnancy_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.maternalarvduringpreg',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_tbroutinehealth_required_cohort_a(self):

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.maternalarvduringpreg',
                subject_identifier=self.subject_identifier,
                visit_code='2000D',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_caregiverphqdeprscreening_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqdeprscreening',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    def test_caregiveredinburghdeprscreening_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiveredinburghdeprscreening',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_ultrasound_required_cohort_a(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.ultrasound',
                subject_identifier=self.subject_identifier,
                visit_code='1000M',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_gad_scoregte_10_referral_required(self):
        visit = MaternalVisit.objects.get(visit_code='1000M')
        mommy.make_recipe('flourish_caregiver.gadanxietyscreening',
                          maternal_visit=visit)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregivergadreferral',
                subject_identifier=self.subject_identifier,
                visit_code='1000M').entry_status, REQUIRED)

    def test_phq9gte_5_referral_required(self):
        visit = MaternalVisit.objects.get(visit_code='1000M')
        mommy.make_recipe('flourish_caregiver.caregiverphqdeprscreening',
                          maternal_visit=visit)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiverphqreferral',
                subject_identifier=self.subject_identifier,
                visit_code='1000M').entry_status, REQUIRED)

    def test_edingte_10_referral_required(self):
        visit = MaternalVisit.objects.get(visit_code='1000M')
        mommy.make_recipe('flourish_caregiver.caregiveredinburghdeprscreening',
                          maternal_visit=visit)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.caregiveredinburghreferral',
                subject_identifier=self.subject_identifier,
                visit_code='1000M').entry_status, REQUIRED)

    @tag('sub')
    def test_hiv_viralload_cd4_required_cohort_a(self):
        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '11123',
            'protocol': 'Tshilo Dikotla'}

        child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'study_maternal_identifier': '11123',
            'study_child_identifier': '1234',
            'dob': get_utcnow() - relativedelta(years=2, months=5)}

        mommy.make_recipe(
            'flourish_child.childdataset',
            **child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
           'flourish_caregiver.maternaldataset',
           **maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            child_dataset_options.get('study_child_identifier'),
            hiv_status=POS)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivviralloadandcd4',
                subject_identifier=subject_identifier,
                visit_code='2000M',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.substanceusepriorpregnancy',
                subject_identifier=subject_identifier,
                visit_code='2000M',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    @tag('hiv')
    def test_hiv_test_required_cohort_a1(self):
        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '11123',
            'protocol': 'Tshilo Dikotla'}

        child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'study_maternal_identifier': '11123',
            'dob': get_utcnow() - relativedelta(years=2, months=5),
            'study_child_identifier': '1234'}

        mommy.make_recipe(
            'flourish_child.childdataset',
            **child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
           'flourish_caregiver.maternaldataset',
           **maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            child_dataset_options.get('study_child_identifier'),
            hiv_status=POS)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivviralloadandcd4',
                subject_identifier=subject_identifier,
                visit_code='2000M',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivrapidtestcounseling',
                subject_identifier=subject_identifier,
                visit_code='2000M',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    @tag('hdsc')
    def test_hiv_disclosure_metadata_required(self):
        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=14),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '11123',
            'protocol': 'Mpepu',
            'preg_pi': 1}

        child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '11123',
            'study_child_identifier': '1234',
            'dob': get_utcnow() - relativedelta(years=14)}

        mommy.make_recipe(
            'flourish_child.childdataset',
            **child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
           'flourish_caregiver.maternaldataset',
           **maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            child_dataset_options.get('study_child_identifier'),
            hiv_status=POS)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivdisclosurestatusa',
                subject_identifier=subject_identifier,
                visit_code='2000M').entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivdisclosurestatusb',
                subject_identifier=subject_identifier,
                visit_code='2000M').entry_status, NOT_REQUIRED)

    @tag('hdsc1')
    def test_hiv_disclosure_ab_metadata_required(self):
        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=11),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '11123',
            'protocol': 'Mpepu',
            'preg_pi': 1}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'twin_triplet': 1,
            'study_maternal_identifier': '11123',
            'study_child_identifier': '1234',
            'dob': get_utcnow() - relativedelta(years=11)}

        self.child_dataset_options1 = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'twin_triplet': 1,
            'study_maternal_identifier': '11123',
            'study_child_identifier': '1236',
            'dob': get_utcnow() - relativedelta(years=11)}

        mommy.make_recipe(
            'flourish_child.childdataset',
            ** self.child_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            ** self.child_dataset_options1)

        maternal_dataset_obj = mommy.make_recipe(
           'flourish_caregiver.maternaldataset',
           **self.maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_twins_assent(
            maternal_dataset_obj.screening_identifier,
            self.child_dataset_options.get('study_child_identifier'),
            self.child_dataset_options1.get('study_child_identifier'),
            hiv_status=POS)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivdisclosurestatusb',
                subject_identifier=subject_identifier,
                visit_code='2000M').entry_status, REQUIRED)

    @tag('hdsc')
    def test_hiv_disclosure_metadata_not_required(self):

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=8),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '11123',
            'protocol': 'Mpepu',
            'preg_pi': 1}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '11123',
            'study_child_identifier': '1234',
            'dob': get_utcnow() - relativedelta(years=8)}

        mommy.make_recipe(
            'flourish_child.childdataset',
            ** self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
           'flourish_caregiver.maternaldataset',
           **self.maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            self.child_dataset_options.get('study_child_identifier'),
            hiv_status=POS)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivdisclosurestatusa',
                subject_identifier=subject_identifier,
                visit_code='2000M').entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivdisclosurestatusb',
                subject_identifier=subject_identifier,
                visit_code='2000M').entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivdisclosurestatusc',
                subject_identifier=subject_identifier,
                visit_code='2000M').entry_status, NOT_REQUIRED)

    @tag('hdsc')
    def test_hiv_disclosure_metadata_not_required2(self):

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=8),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-uninfected',
            'study_maternal_identifier': '11123',
            'protocol': 'Mpepu'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Unexposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '11123',
            'study_child_identifier': '1234',
            'dob': get_utcnow() - relativedelta(years=8)}

        mommy.make_recipe(
            'flourish_child.childdataset',
            ** self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
           'flourish_caregiver.maternaldataset',
           **self.maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            self.child_dataset_options.get('study_child_identifier'),
            hiv_status=NEG)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivdisclosurestatusa',
                subject_identifier=subject_identifier,
                visit_code='2000M').entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivdisclosurestatusb',
                subject_identifier=subject_identifier,
                visit_code='2000M').entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivdisclosurestatusc',
                subject_identifier=subject_identifier,
                visit_code='2000M').entry_status, NOT_REQUIRED)

    def test_hiv_rapid_test_required(self):

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=8),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-uninfected',
            'study_maternal_identifier': '11123',
            'protocol': 'Mpepu',
            'preg_pi': 0}

        self.child_dataset_options = {
            'infant_hiv_exposed': '',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '11123',
            'study_child_identifier': '1234',
            'dob': get_utcnow() - relativedelta(years=8)}

        mommy.make_recipe(
            'flourish_child.childdataset',
            ** self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
           'flourish_caregiver.maternaldataset',
           **self.maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            self.child_dataset_options.get('study_child_identifier'),
            hiv_status=NEG)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivrapidtestcounseling',
                subject_identifier=subject_identifier,
                visit_code='2000M').entry_status, REQUIRED)

    @tag('rtt')
    def test_hiv_rapid_test_not_required(self):

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=8),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-uninfected',
            'study_maternal_identifier': '11123',
            'protocol': 'Mpepu',
            'preg_pi': 0}

        self.child_dataset_options = {
            'infant_hiv_exposed': '',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '11123',
            'study_child_identifier': '1234',
            'dob': get_utcnow() - relativedelta(years=8)}

        mommy.make_recipe(
            'flourish_child.childdataset',
            ** self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
           'flourish_caregiver.maternaldataset',
           **self.maternal_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            self.child_dataset_options.get('study_child_identifier'),
            hiv_status=POS)

        history_model = 'edc_visit_schedule.subjectschedulehistory'

        history_obj = django_apps.get_model(history_model).objects.get(
            subject_identifier=subject_identifier)

        history_obj.offschedule_datetime = get_utcnow().date() + relativedelta(days=100)
        history_obj.save()

        visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            report_datetime=get_utcnow(),
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.hivrapidtestcounseling',
            maternal_visit=visit,
            rapid_test_done=YES,
            result_date=get_utcnow().date(),
            result=NEG)

        visit2 = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2001M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow() + relativedelta(days=91),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivrapidtestcounseling',
                subject_identifier=subject_identifier,
                visit_code='2001M').entry_status, REQUIRED)

        mommy.make_recipe(
            'flourish_caregiver.hivrapidtestcounseling',
            maternal_visit=visit2,
            rapid_test_done=YES,
            result_date=get_utcnow().date() + relativedelta(days=91),
            result=NEG)

        visit2 = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2002M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.hivrapidtestcounseling',
                subject_identifier=subject_identifier,
                visit_code='2002M').entry_status, NOT_REQUIRED)
    @tag('bf')
    def test_b_freeding_required(self):
        
        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.subject_consent.subject_identifier,
            live_infants_to_register=1)
        
        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)
        
        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(visit_code='2001M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)
        
        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(visit_code='2002M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_caregiver.breastfeedingquestionnaire',
                subject_identifier=self.subject_identifier,
                visit_code='2002M').entry_status, REQUIRED)