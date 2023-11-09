from dateutil.relativedelta import relativedelta
from django.test import tag, TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import NEG, POS, YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from ..helper_classes import MaternalStatusHelper
from ..identifiers import ScreeningIdentifier
from ..subject_helper_mixin import SubjectHelperMixin


@tag('msh')
class TestMaternalStatusHelper(TestCase):

    def setUp(self):
        import_holidays()
        self.options = {
            'consent_datetime': get_utcnow(),
            'breastfeed_intent': YES,
            'version': '1'}

        screening_identifier = ScreeningIdentifier().identifier

        mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=screening_identifier,
            version='1',
            child_version='1')

        self.screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',
            screening_identifier=screening_identifier)
        self.screening_preg.save()

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=self.screening_preg.screening_identifier,
            **self.options)

        self.subject_consent.save()

        self.child_consent=mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            child_dob=None,
            first_name=None,
            last_name=None, )

    def test_enrollment_hiv_status_pregnant_pos_valid(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            enrollment_hiv_status=POS,
            child_subject_identifier=self.child_consent.subject_identifier,
            subject_identifier=self.subject_consent.subject_identifier, )

        status_helper = MaternalStatusHelper(
            subject_identifier=self.subject_consent.subject_identifier)

        self.assertEqual(status_helper.hiv_status, POS)

    def test_enrollment_hiv_status_pregnant_neg_valid(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            enrollment_hiv_status=NEG,
            week32_test=YES,
            week32_test_date=get_utcnow().date(),
            current_hiv_status=NEG,
            child_subject_identifier=self.child_consent.subject_identifier,
            subject_identifier=self.subject_consent.subject_identifier)

        status_helper = MaternalStatusHelper(
            subject_identifier=self.subject_consent.subject_identifier)

        self.assertEqual(status_helper.hiv_status, NEG)

    @tag('eppv')
    def test_enrollment_prior_participant_valid(self):
        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'screening_identifier': '111111',
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '89721',
            'protocol': 'Tshilo Dikotla'}

        child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '89721',
            'study_child_identifier': '1234'}

        mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **maternal_dataset_options)

        child_dataset_obj = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=2, months=5),
            **child_dataset_options)

        sh = SubjectHelperMixin()

        subject_identifier = sh.create_TD_efv_enrollment(
            maternal_dataset_options.get('screening_identifier'),
            child_dataset_obj.study_child_identifier)

        status_helper = MaternalStatusHelper(
            subject_identifier=subject_identifier)

        self.assertEqual(status_helper.hiv_status, POS)
