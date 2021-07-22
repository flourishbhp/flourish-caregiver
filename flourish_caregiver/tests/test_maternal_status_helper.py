from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NEG, POS
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from ..subject_helper_mixin import SubjectHelperMixin
from ..helper_classes import MaternalStatusHelper


@tag('msh')
class TestMaternalStatusHelper(TestCase):

    databases = '__all__'

    def setUp(self):
        import_holidays()

    def test_enrollment_hiv_status_pregnant_pos_valid(self):

        screening_obj = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_obj.screening_identifier)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier)

        status_helper = MaternalStatusHelper(
            subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(status_helper.hiv_status, POS)

    def test_enrollment_hiv_status_pregnant_neg_valid(self):

        screening_obj = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_obj.screening_identifier)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            enrollment_hiv_status=NEG,
            subject_identifier=subject_consent.subject_identifier)

        status_helper = MaternalStatusHelper(
            subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(status_helper.hiv_status, POS)

    def test_enrollment_prior_participant_valid(self):

        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '89721',
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=2, months=5),
            **self.child_dataset_options)

        sh = SubjectHelperMixin()

        maternal_dataset = sh.create_TD_efv_enrollment(
            maternal_dataset_options.get('screening_identifier'))

        subject_identifier = sh.enroll_prior_participant(
            maternal_dataset.screening_identifier)

        status_helper = MaternalStatusHelper(
            subject_identifier=subject_identifier)

        self.assertEqual(status_helper.hiv_status, POS)
