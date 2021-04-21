import re
from dateutil.relativedelta import relativedelta

from django.apps import apps as django_apps
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from edc_constants.constants import YES, NO, NOT_APPLICABLE

from ..subject_helper_mixin import SubjectHelperMixin

subject_identifier = '[B|C]142\-[0-9\-]+'


class TestInfantSubjectIdentifier(TestCase):

    def setUp(self):
        import_holidays()

        self.subject_helper = SubjectHelperMixin()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.child_dummy_consent_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')

        self.caregiver_child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

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

    def test_infant_subject_identifier_generated(self):
        """Test consent allocates subject identifier starting with a B for a
        biological mother.
        """
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=4,
                                                                                months=5)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            screening_identifier='123456',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=4, months=5),
            ** self.child_dataset_options)

        self.subject_helper.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier)

        self.assertTrue(
            re.match(
                subject_identifier,
                self.child_dummy_consent_cls.objects.all()[0].subject_identifier))

    def test_infant_subject_identifier_2_children(self):
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=4,
                                                                                months=9)
        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=4, months=9),
            **self.child_dataset_options)

        self.child_dataset_options['study_child_identifier'] = '1235'
        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=5, months=9),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        first_child = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=(get_utcnow() - relativedelta(years=4, months=9)).date(),)

        second_child = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            identity='234513181',
            confirm_identity='234513181',
            child_dob=(get_utcnow() - relativedelta(years=5, months=9)).date(),)

        self.assertTrue(first_child.subject_identifier.endswith('10'))
        self.assertTrue(second_child.subject_identifier.endswith('20'))

    def test_infant_subject_identifier_assent(self):
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(
            years=7, months=5)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            screening_identifier='123456',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=7, months=5),
            ** self.child_dataset_options)

        self.subject_helper.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier)

        self.assertTrue(
            re.match(
                subject_identifier,
                self.child_dummy_consent_cls.objects.all()[0].subject_identifier))
