import pytz
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import tag, TestCase
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from ..models import FlourishConsentVersion
from ..models import OnScheduleCohortBEnrollment, SubjectConsent
from ..subject_helper_mixin import SubjectHelperMixin


@tag('src4')
class TestSubjectReConsent(TestCase):
    databases = '__all__'
    utc = pytz.UTC

    def year_3_age(self, year_3_years, year_3_months):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        child_dob = start_date_year_3 - relativedelta(years=year_3_years,
                                                      months=year_3_months)
        return child_dob

    def setUp(self):
        import_holidays()

        self.study_maternal_identifier = '981232'

        self.maternal_dataset_options = {
            'delivdt': self.year_3_age(5, 1),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'mom_pregarv_strat': '3-drug ART',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Mpepu'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        self.maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=self.year_3_age(5, 1),
            **self.child_dataset_options)

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '3'}

        sh = SubjectHelperMixin()

        self.subject_identifier = sh.enroll_prior_participant(
            self.maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            version='3',
            child_version='3')

        self.flourish_consent_version = FlourishConsentVersion.objects.get(
            screening_identifier=self.maternal_dataset_obj.screening_identifier)

    def test_reconsent_participant(self):
        self.flourish_consent_version.version = '4'
        self.flourish_consent_version.save()

        self.options.update(version='4')

        mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            subject_identifier=self.subject_identifier,
            **self.options)

        self.assertEqual(SubjectConsent.objects.filter(
            subject_identifier=self.subject_identifier).count(), 2)
        self.assertTrue(SubjectConsent.objects.filter(
            subject_identifier=self.subject_identifier, version='3').exists())
        self.assertTrue(SubjectConsent.objects.filter(
            subject_identifier=self.subject_identifier, version='4').exists())

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=self.subject_identifier).count(), 1)

    def test_v4_consent(self):
        self.maternal_dataset_options.update(study_maternal_identifier='1234')
        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            **self.maternal_dataset_options)

        self.child_dataset_options.update(
            study_maternal_identifier='1234',
            study_child_identifier='4321')

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=self.year_3_age(5, 1),
            **self.child_dataset_options)

        options = {
            'consent_datetime': get_utcnow(),
            'version': '4'}

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=YES,
            **options)

        study_child_identifier = self.child_dataset_options['study_child_identifier']
        mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt, )

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        self.assertEqual(SubjectConsent.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)
        self.assertTrue(SubjectConsent.objects.filter(
            subject_identifier=self.subject_identifier, version='4').exists())
