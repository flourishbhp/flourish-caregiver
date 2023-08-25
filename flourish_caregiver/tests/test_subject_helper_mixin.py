from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from ..models import MaternalDataset, ScreeningPriorBhpParticipants, SubjectConsent
from ..models import OnScheduleCohortBEnrollment, OnScheduleCohortBQuarterly
from ..models import OnScheduleCohortCEnrollment, OnScheduleCohortCQuarterly
from ..subject_helper_mixin import SubjectHelperMixin


@tag('sh')
class TestSubjectHelperMixin(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_helper = SubjectHelperMixin()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '89721',
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '89721',
            'study_child_identifier': '1234'}

    def test_create_antenatal_enrollment(self):

        subject_identifier = self.subject_helper.create_antenatal_enrollment()

        self.assertEqual(SubjectConsent.objects.filter(
            subject_identifier=subject_identifier).count(), 1)

    def test_td_prior_participant_creation(self):

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            screening_identifier='123458',
            ** self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=2, months=5),
            **self.child_dataset_options)

        self.subject_helper.create_TD_efv_enrollment(
            screening_identifier=maternal_dataset_obj.screening_identifier)

        self.assertEqual(
            ScreeningPriorBhpParticipants.objects.all().count(), 1)

        self.assertEqual(MaternalDataset.objects.all().count(), 1)

        self.assertEqual(SubjectConsent.objects.all().count(), 1)

    def test_prepare_prior_participant_enrollmment(self):

        self.maternal_dataset_options['mom_hivstatus'] = 'HIV-uninfected'

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            screening_identifier='123459',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            **self.child_dataset_options)

        self.subject_helper.prepare_prior_participant_enrollment(
            maternal_dataset_obj)

        logentry_cls = django_apps.get_model('flourish_follow.logentry')

        self.assertEqual(logentry_cls.objects.all().count(), 1)

    def test_enroll_prior_participant_cohort_b(self):

        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=4,
                                                                                months=5)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            screening_identifier='123456',
            **self.maternal_dataset_options)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=4, months=5),
            **self.child_dataset_options)

        subject_identifier = self.subject_helper.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            child_dataset.study_child_identifier)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_fu1_schedule1').count(), 1)

    @tag('sh1')
    def test_enroll_prior_participant_assent_cohort_b(self):

        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=7,
                                                                                months=5)
        self.maternal_dataset_options['protocol'] = 'Mpepu'

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            screening_identifier='123453',
            **self.maternal_dataset_options)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=7, months=5),
            **self.child_dataset_options)

        subject_identifier = self.subject_helper.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            child_dataset.study_child_identifier)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_quarterly1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_fu1_schedule1').count(), 1)

    def test_enroll_prior_participant_assent_cohort_c(self):

        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=10,
                                                                                months=5)
        self.maternal_dataset_options['protocol'] = 'Mma Bana'

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            screening_identifier='123452',
            preg_pi=1,
            **self.maternal_dataset_options)

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=5),
            **self.child_dataset_options)

        subject_identifier = self.subject_helper.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            child_dataset.study_child_identifier)

        self.assertEqual(OnScheduleCohortCEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='c_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortCQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='c_quarterly1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortCEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='c_fu1_schedule1').count(), 1)
