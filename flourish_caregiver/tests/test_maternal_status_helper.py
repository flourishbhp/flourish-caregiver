from django.test import TestCase, tag
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

    # def test_enrollment_prior_participant_valid(self):
    #
        # sh = SubjectHelperMixin()
        #
        # maternal_dataset = sh.create_TD_efv_enrollment()
        #
        # subject_identifier = sh.enroll_prior_participant(
            # maternal_dataset.screening_identifier)
            #
        # status_helper = MaternalStatusHelper(
            # subject_identifier=subject_identifier)
            #
        # self.assertEqual(status_helper.hiv_status, POS)
