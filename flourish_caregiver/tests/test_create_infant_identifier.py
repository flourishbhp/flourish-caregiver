import re
from dateutil.relativedelta import relativedelta

from django.apps import apps as django_apps
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from edc_constants.constants import NO, YES

from ..subject_helper_mixin import SubjectHelperMixin

subject_identifier = '[B|C]142\-[0-9\-]+'


class TestInfantSubjectIdentifier(TestCase):

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


    def test_infant_subject_identifier_generated(self):
        """Test consent allocates subject identifier starting with a B for a 
        biological mother.
        """
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=4, months=5)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            screening_identifier='123456',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            **self.child_dataset_options)

        self.subject_helper.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier)
        
        child_dummy_consent_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')

        self.assertTrue(
            re.match(
                subject_identifier,
                child_dummy_consent_cls.objects.all()[0].subject_identifier))



