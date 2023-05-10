from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.contrib.auth.models import Group, User
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES, NO, OTHER
from edc_facility.import_holidays import import_holidays
from edc_visit_schedule.models import SubjectScheduleHistory
from edc_visit_schedule.constants import ON_SCHEDULE
from edc_visit_tracking.constants import SCHEDULED
from edc_registration.models import RegisteredSubject
from flourish_prn.models import CaregiverOffStudy
from flourish_child.models import Appointment as ChildAppointment
from model_mommy import mommy

from ..models import SubjectConsent, OnScheduleCohortBEnrollment, OnScheduleCohortBQuarterly, CaregiverOffSchedule
from ..models import CaregiverLocator, MaternalDataset, ScreeningPriorBhpParticipants
from ..helper_classes import CaregiverBiologicalSwitch


@tag('biological')
class TestCaregiverBiologicalSwitch(TestCase):

    def year_3_age(self, year_3_years, year_3_months):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        child_dob = start_date_year_3 - relativedelta(years=year_3_years,
                                                      months=year_3_months)
        return child_dob

    def setUp(self):
        # Create the assignable user and group for testing.
        app_config = django_apps.get_app_config('flourish_follow')
        Group.objects.create(name=app_config.assignable_users_group)
        User.objects.create(username='flourish')
        import_holidays()

        self.study_maternal_identifier = '981232'

        self.maternal_dataset_options = {
            'delivdt': self.year_3_age(5, 1),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Mpepu'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=self.year_3_age(5, 1),
            **self.child_dataset_options)

        try:
            CaregiverLocator.objects.get(
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,)
        except CaregiverLocator.DoesNotExist:
            mommy.make_recipe(
                'flourish_caregiver.caregiverlocator',
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,
                screening_identifier=maternal_dataset_obj.screening_identifier)

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '3'}

        self.flourish_consent_version = mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version='3')

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            biological_caregiver=NO,
            **self.options)

        self.subject_identifier = subject_consent.subject_identifier

        study_child_identifier = self.child_dataset_options['study_child_identifier']

        childconsent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt,)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=ChildAppointment.objects.get(
                visit_code='2000',
                subject_identifier=childconsent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.switch_cls = CaregiverBiologicalSwitch(caregiver_sid=self.subject_identifier)

    def test_caregiver_child_pair_enrolled(self):
        self.assertEqual(SubjectConsent.objects.filter(
            subject_identifier=self.subject_identifier).count(), 1)
        self.assertTrue(SubjectConsent.objects.filter(
            subject_identifier=self.subject_identifier, biological_caregiver=NO).exists())

        child_consent = SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier).caregiverchildconsent_set.all()
        self.assertTrue(child_consent.exists())

        self.assertTrue(self.subject_identifier.startswith('C'))

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_identifier, schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=self.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=self.subject_identifier).count(), 1)

    def test_caregiver_biological_switch(self):

        caregiver_offstudy = self.switch_cls.take_caregiver_offstudy(
            report_dt=get_utcnow(),
            offstudy_dt=get_utcnow().date(),
            reason=OTHER,
            reason_othr='Biological mother taking over', )

        # Assert caregiver is correctly taken off study
        self.assertTrue(caregiver_offstudy)
        self.assertEqual(CaregiverOffStudy.objects.filter(
            subject_identifier=self.subject_identifier, ).count(), 1)
        self.assertEqual(CaregiverOffSchedule.objects.filter(
            subject_identifier=self.subject_identifier, ).count(), 2)
        self.assertFalse(SubjectScheduleHistory.objects.filter(
            subject_identifier=self.subject_identifier,
            offschedule_datetime__isnull=True,
            schedule_status=ON_SCHEDULE).exists())

        # Create a locator instance for the biological mother, with new screening
        # identifier and update maternal dataset object with identifier.
        self.switch_cls.create_bio_mother_locator(
            report_dt=get_utcnow(), signed_dt=get_utcnow().date())

        self.assertIsNotNone(self.switch_cls.biological_mother_locator)
        dataset = MaternalDataset.objects.filter(
            screening_identifier=self.switch_cls.screening_identifier)
        self.assertTrue(dataset.exists())
        self.assertEqual(
            dataset[0].screening_identifier, self.switch_cls.screening_identifier)

        # Create an instance of the BHP prior screening for the mother
        screening_options = {
            'child_alive': YES,
            'mother_alive': YES,
            'flourish_participation': 'interested'}
        mother_screening = self.switch_cls.create_bio_screening(
            report_dt=get_utcnow(), **screening_options)
        self.assertIsNotNone(mother_screening)
        self.assertEqual(
            mother_screening.study_maternal_identifier, dataset[0].study_maternal_identifier)
        self.assertEqual(
            mother_screening.screening_identifier, dataset[0].screening_identifier)

        # Consent the mother to the study
        consent_options = {
            'language': 'en',
            'recruit_source': 'BHP recruiter/clinician',
            'recruitment_clinic': 'Prior',
            'is_literate': YES,
            'dob': get_utcnow() - relativedelta(years=26),
            'is_dob_estimated': NO,
            'citizen': YES,
            'identity': '123422211',
            'identity_type': 'country_id',
            'confirm_identity': '123422211',
            'remain_in_study': YES,
            'hiv_testing': NOT_APPLICABLE,
            'breastfeed_intent': NOT_APPLICABLE,
            'child_consent': YES,
            'future_contact': YES,
            'consent_reviewed': YES,
            'study_questions': YES,
            'assessment_score': YES,
            'consent_signature': YES,
            'consent_copy': YES,
            'consent_datetime': get_utcnow()}
        self.switch_cls.create_bio_consent(**consent_options)

        self.assertIsNotNone(self.switch_cls.biological_mother_consent)
        self.assertTrue(ScreeningPriorBhpParticipants.objects.filter(
            subject_identifier=self.switch_cls.biological_mother_consent.subject_identifier).exists())
        self.assertEqual(self.subject_identifier.replace('C', 'B'),
                         self.switch_cls.biological_mother_consent.subject_identifier)
        self.assertEqual(self.switch_cls.biological_mother_consent.caregiverchildconsent_set.count(), 0)
        self.assertEqual(SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier).caregiverchildconsent_set.count(), 1)

        biological_sid = self.switch_cls.biological_mother_consent.subject_identifier
        # Add the child consent to the biological mother, removing it from the caregiver
        self.switch_cls.add_child_consent_to_mother()
        self.assertEqual(
            self.switch_cls.biological_mother_consent.caregiverchildconsent_set.count(), 1)
        self.assertEqual(SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier).caregiverchildconsent_set.count(), 0)

        self.assertEqual(
            RegisteredSubject.objects.filter(relative_identifier=self.subject_identifier).count(), 1)
        self.assertEqual(
            RegisteredSubject.objects.filter(relative_identifier=biological_sid).count(), 0)

        # Update biological mother's ID to the child's registered subject object
        self.switch_cls.update_child_registered_subject()

        self.assertEqual(
            RegisteredSubject.objects.filter(relative_identifier=self.subject_identifier).count(), 0)
        self.assertEqual(
            RegisteredSubject.objects.filter(relative_identifier=biological_sid).count(), 1)

        # Create instance of the biological mother's previous enrollment information
        prev_enrol_defaults = {'maternal_prev_enroll': 'YES'}
        self.switch_cls.create_bio_previous_enrol_info(
            report_dt=get_utcnow(), **prev_enrol_defaults)

        # Put mother on the enrolment schedule
        self.switch_cls.put_on_enrol_schedule(onschedule_dt=get_utcnow())
        self.assertEqual(Appointment.objects.filter(
            subject_identifier=biological_sid, schedule_name='b_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBEnrollment.objects.filter(
            subject_identifier=biological_sid).count(), 1)

        # Put mother on the quarterly schedule
        self.switch_cls.put_on_quart_schedule(onschedule_dt=get_utcnow())
        self.assertEqual(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=biological_sid).count(), 1)
