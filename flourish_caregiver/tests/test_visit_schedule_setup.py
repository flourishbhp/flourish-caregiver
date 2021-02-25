from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from edc_appointment.models import Appointment

from ..models import OnScheduleCohortA, OnScheduleCohortB, OnScheduleCohortC
from ..models import OnSchedulePool
from flourish_child.models import ChildDataset
from pre_flourish.models import PreFlourishConsent


@tag('vs')
class TestVisitScheduleSetup(TestCase):

    databases = '__all__'

    def setUp(self):
        import_holidays()
        self.subject_identifier = '12345678'

        self.options = {
            'consent_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'mom_enrolldate': get_utcnow(),
            'study_child_identifier': '1234',
            'mom_hivstatus': 'HIV-infected',
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_child_identifier': '1234'}


    @tag('sb')
    def test_cohort_a_onschedule_antenatal_valid(self):

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier,)

        self.assertEqual(OnScheduleCohortA.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortA.objects.get(
            subject_identifier=subject_consent.subject_identifier).schedule_name, 'cohort_a_schedule1')

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 0)

#     @tag('sb')
    def test_cohort_a_onschedule_consent_valid(self):
        self.subject_identifier = self.subject_identifier[:-1] + '1'
        self.options['subject_identifier'] = self.subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_identifier=self.subject_identifier,
            dob=get_utcnow() - relativedelta(years=2, months=5))

        self.assertEqual(OnScheduleCohortA.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortA.objects.get(
            subject_identifier=caregiver_child_consent.subject_identifier).schedule_name,
            'cohort_a_schedule1')

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(), 0)


    def test_cohort_b_onschedule_valid(self):

        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=5, months=2)
        self.options['subject_identifier'] = self.subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_identifier=self.subject_identifier,
            dob=get_utcnow() - relativedelta(years=5, months=2))

        self.assertEqual(OnScheduleCohortB.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortB.objects.get(
            subject_identifier=caregiver_child_consent.subject_identifier).schedule_name,
            'cohort_b_schedule1')

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(), 0)

    def test_cohort_b_assent_onschedule_valid(self):

        self.subject_identifier = self.subject_identifier[:-1] + '3'
        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=7, months=2)
        self.options['subject_identifier'] = self.subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_identifier=self.subject_identifier,
            dob=get_utcnow() - relativedelta(years=7, months=2))

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=self.subject_identifier + '-10',
            dob=get_utcnow() - relativedelta(years=7, months=2),
            version=caregiver_child_consent.version)

        self.assertEqual(OnScheduleCohortB.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortB.objects.get(
            subject_identifier=caregiver_child_consent.subject_identifier).schedule_name,
            'cohort_b_schedule1')

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(), 0)

    def test_cohort_c_onschedule_valid(self):
        self.subject_identifier = self.subject_identifier[:-1] + '4'

        self.maternal_dataset_options['protocol'] = 'Mashi'
        self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=10, months=2)
        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'
        self.options['subject_identifier'] = self.subject_identifier

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            ** self.options)

#         PreFlourishConsent.objects.using('pre_flourish').create(
#                                                         identity=subject_consent.identity,
#                                                         confirm_identity=subject_consent.identity,
#                                                         dob=get_utcnow() - relativedelta(years=25),
#                                                         first_name=subject_consent.first_name,
#                                                         last_name=subject_consent.last_name,
#                                                         initials=subject_consent.initials,
#                                                         gender='F',
#                                                         identity_type='OMANG',
#                                                         is_dob_estimated='-',
#                                                         version='1',
#                                                         consent_datetime=get_utcnow(),
#                                                         created=get_utcnow())

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_identifier=self.subject_identifier,
            dob=get_utcnow() - relativedelta(years=10, months=2))

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=self.subject_identifier + '-10',
            dob=get_utcnow() - relativedelta(years=10, months=2),
            version=caregiver_child_consent.version)

        self.assertEqual(OnScheduleCohortC.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortC.objects.get(
            subject_identifier=caregiver_child_consent.subject_identifier).schedule_name,
            'cohort_c_schedule1')

        self.assertNotEqual(Appointment.objects.filter(
            subject_identifier=caregiver_child_consent.subject_identifier).count(), 0)

#     def test_pool_onschedule_valid(self):
#         self.subject_identifier = self.subject_identifier[:-1] + '5'
#         self.maternal_dataset_options['protocol'] = 'Mashi'
#         self.maternal_dataset_options['delivdt'] = get_utcnow() - relativedelta(years=9, months=2)
#         self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'
#         self.options['subject_identifier'] = self.subject_identifier
#
#         mommy.make_recipe(
#             'flourish_child.childdataset',
#             subject_identifier=self.subject_identifier + '10',
#             **self.child_dataset_options)
#
#         mommy.make_recipe(
#             'flourish_caregiver.maternaldataset',
#             subject_identifier=self.subject_identifier,
#             **self.maternal_dataset_options)
#
#         mommy.make_recipe(
#             'flourish_caregiver.subjectconsent',
#             ** self.options)
#
#         caregiver_child_consent = mommy.make_recipe(
#             'flourish_caregiver.caregiverchildconsent',
#             subject_identifier=self.subject_identifier,
#             dob=get_utcnow() - relativedelta(years=9, months=2))
#
#         self.assertEqual(OnSchedulePool.objects.filter(
#             subject_identifier=caregiver_child_consent.subject_identifier).count(), 1)
#
#         self.assertEqual(OnSchedulePool.objects.get(
#             subject_identifier=caregiver_child_consent.subject_identifier).schedule_name,
#             'pool_schedule1')
#
#         self.assertNotEqual(Appointment.objects.filter(
#             subject_identifier=caregiver_child_consent.subject_identifier).count(), 0)
