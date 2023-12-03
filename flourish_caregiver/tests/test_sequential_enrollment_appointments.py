import pytz
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.db import models
from django.test import tag, TestCase
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import DONE
from edc_facility.import_holidays import import_holidays
from edc_visit_schedule import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_caregiver.helper_classes.cohort import Cohort
from flourish_caregiver.helper_classes.sequential_onschedule_mixin import \
    SeqEnrolOnScheduleMixin
from flourish_caregiver.helper_classes.sequential_subject_helper import \
    SequentialSubjectHelper
from flourish_caregiver.models import MaternalDataset, \
    OnScheduleCohortAEnrollment, \
    OnScheduleCohortAQuarterly, OnScheduleCohortBSec, \
    OnScheduleCohortBSecQuart
from ..helper_classes.onschedule_helper import OnScheduleHelper
from flourish_child.models import ChildDataset
from flourish_caregiver.helper_classes.schedule_dict import caregiver_schedule_dict



@tag('seqappt')
class TestSequentialEnrollmentAppointments(TestCase):
    databases = '__all__'
    utc = pytz.UTC

    def setUp(self):
        import_holidays()

        self.subject_identifier = '12345678'
        self.study_maternal_identifier = '89721'

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'mom_pregarv_strat': '3-drug ART',
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        self.child_dummy_consent_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')

        self.sequential_helper = SequentialSubjectHelper(
            child_dataset_options=self.child_dataset_options,
            maternal_dataset_options=self.maternal_dataset_options
        )

    @tag('zlz')
    def test_delete_completed_appointments(self):
        """Test function to delete completed appointments for a subject from one
        schedule and add to another schedule. The function performs the following tasks:
            1. Retrieves subject identifier
            2. Asserts that the subject identifier is not None
            3. Asserts that the OnScheduleCohortAEnrollment database has an object with
            matching subject identifier and 'a_enrol1_schedule1' schedule name
            4. Asserts that the OnScheduleCohortAQuarterly database has 0 objects with
            matching subject identifier and 'a_quarterly1_schedule1' schedule name
            5. Creates a MaternalVisit object for the subject and
            'a_quarterly1_schedule1' schedule name, then asserts that the
            OnScheduleCohortAQuarterly database has 1 object with matching subject
            identifier and 'a_quarterly1_schedule1' schedule name
            6. Filters appointments for the subject with 'a_quarterly1_schedule1'
            schedule name, and creates maternal visit objects for all appointments
            except the last 5. Sets appointment status to 'DONE' for each completed
            appointment.
            7. Removes the caregiver from the 'quarterly' type schedule for 'cohort_a'
            cohort and 'child_count' of 1.
            8. Updates subject and caregiver-child consents, maternal dataset object,
            child dataset object, and Cohort object variables. Adds the Cohort object
            onto the 'b_sec1_schedule1' schedule, then asserts that the subject is on
            the 'b_sec1_schedule1' schedule and has 1 related appointment.
            9. Asserts that the OnScheduleCohortBSecQuart database has 0 objects with
            matching subject identifier and 'b_sec_quart1_schedule1' schedule name,
            creates a MaternalVisit object for the subject and 'b_sec1_schedule1'
            schedule name, then asserts that the OnScheduleCohortBSecQuart
            database has 1 object with matching subject identifier and
            'b_sec_quart1_schedule1' schedule name.
            10. Deletes completed appointments from the 'a_quarterly1_schedule1'
            schedule for the subject and adds them to the 'b_sec_quart1_schedule1'
            schedule. Asserts that no appointments exist for the subject in both
            schedules.
            """
        subject_identifier = self.sequential_helper.get_cohort_a_subj()
        self.assertNotEqual(subject_identifier, None)
        self.assertEqual(OnScheduleCohortAEnrollment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='a_enrol1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='a_quarterly1_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                schedule_name='a_enrol1_schedule1',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='a_quarterly1_schedule1').count(), 1)

        quarterly_appointments = Appointment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='a_quarterly1_schedule1'
        )

        for x in range(0, quarterly_appointments.count() - 5):
            appointment = quarterly_appointments[x]
            mommy.make_recipe(
                'flourish_caregiver.maternalvisit',
                appointment=appointment,
                report_datetime=get_utcnow(),
                reason=SCHEDULED)
            appointment.status = DONE
            appointment.save()

        # self.take_off_caregiver_offschedule(subject_identifier=subject_identifier,
        #                                     cohort='cohort_a',
        #                                     schedule_type='quarterly', child_count='1')

        subject_consent = self.sequential_helper.update_consent(
            subject_identifier=subject_identifier)
        caregiver_child_consent_obj = self.sequential_helper \
            .update_caregiver_child_consent(
            subject_consent, self.sequential_helper.year_3_age(7, 1))
        maternal_dataset_obj = MaternalDataset.objects.get(
            subject_identifier=subject_identifier)
        child_dataset_obj = ChildDataset.objects.get(
            study_maternal_identifier=maternal_dataset_obj
            .study_maternal_identifier)
        cohort = Cohort(
            child_dob=self.sequential_helper.year_3_age(7, 1),
            enrollment_date=subject_consent.created.date(),
            infant_hiv_exposed=child_dataset_obj.infant_hiv_exposed,
            protocol=maternal_dataset_obj.protocol,
            mum_hiv_status=maternal_dataset_obj.mom_hivstatus,
            dtg=maternal_dataset_obj.preg_dtg,
            efv=maternal_dataset_obj.preg_efv,
            pi=maternal_dataset_obj.preg_pi).cohort_variable

        helper_cls = OnScheduleHelper(
            subject_identifier=caregiver_child_consent_obj.subject_identifier,
            cohort=cohort)
        helper_cls.put_cohort_onschedule(
            caregiver_child_consent_obj,
            base_appt_datetime=get_utcnow() + relativedelta(years=1, months=1))

        self.assertEqual(OnScheduleCohortBSec.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_sec1_schedule1').count(), 1)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_sec1_schedule1').count(), 1)

        self.assertEqual(OnScheduleCohortBSecQuart.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_sec_quart1_schedule1').count(), 0)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='2000M',
                schedule_name='b_sec1_schedule1',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleCohortBSecQuart.objects.filter(
            subject_identifier=subject_consent.subject_identifier,
            schedule_name='b_sec_quart1_schedule1').count(), 1)

        sq_onschedule_mixin = SeqEnrolOnScheduleMixin()

        sq_onschedule_mixin.delete_completed_appointments(
            appointment_model_cls=Appointment,
            subject_identifier=subject_identifier,
            schedule_name='b_sec_quart1_schedule1')

        prev_appts = Appointment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='a_quarterly1_schedule1'
        ).values_list('visit_code', flat=True)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name='b_sec_quart1_schedule1',
            visit_code__in=prev_appts
        ).count(), 0)

    # def take_off_caregiver_offschedule(self, subject_identifier, cohort, schedule_type,
    #                                    child_count):
    #     onschedule_model = caregiver_schedule_dict[cohort][schedule_type][
    #         'onschedule_model']
    #     schedule_name = caregiver_schedule_dict[cohort][schedule_type][child_count]
    #
    #     _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
    #         onschedule_model=onschedule_model,
    #         name=schedule_name)
    #     schedule.take_off_schedule(
    #         subject_identifier=subject_identifier,
    #         schedule_name=schedule_name)
