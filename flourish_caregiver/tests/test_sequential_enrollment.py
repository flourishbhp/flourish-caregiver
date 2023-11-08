from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_appointment.constants import INCOMPLETE_APPT
from edc_base import get_utcnow
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import SCHEDULED
from flourish_child.models import Appointment as ChildAppointment
from flourish_child.models import (OnScheduleChildCohortAQuarterly, OnScheduleChildCohortBEnrollment,
                                   OnScheduleChildCohortBQuarterly, ChildOffSchedule,
                                   OnScheduleChildCohortCQuarterly, OnScheduleChildCohortAFU,
                                   OnScheduleChildCohortBFUSeq, OnScheduleChildCohortCFUSeq,
                                   OnScheduleChildCohortBSecSeq)
from flourish_child.helper_classes.child_fu_onschedule_helper import ChildFollowUpEnrolmentHelper

from model_mommy import mommy
from dateutil.relativedelta import relativedelta

from ..models import MaternalDataset
from ..models import (OnScheduleCohortAEnrollment, OnScheduleCohortAQuarterly,
                      OnScheduleCohortBEnrollment, OnScheduleCohortBQuarterly,
                      SubjectConsent, CaregiverOffSchedule, OnScheduleCohortCQuarterly,
                      OnScheduleCohortAFU, OnScheduleCohortBFUSeq, OnScheduleCohortCFUSeq,
                      OnScheduleCohortBSecSeq)
from ..helper_classes import SequentialCohortEnrollment
from ..subject_helper_mixin import SubjectHelperMixin


@tag('sqec')
class TestSequentialEnrollment(TestCase):

    def setUp(self):
        import_holidays()
        self.study_maternal_identifier = '89721'

        self.options = {
            'consent_datetime': get_utcnow() - relativedelta(years=1),
            'version': '3'}

        child_consent_options = {
            'consent_datetime': get_utcnow() - relativedelta(years=1)}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=5, months=1),
            'mom_enrolldate': get_utcnow() - relativedelta(years=5,  months=11),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Tshilo Dikotla',
            'mom_pregarv_strat': '3-drug ART'}

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow() - relativedelta(years=5, months=11),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=5, months=1),
            **self.child_dataset_options)

        self.subject_helper_cls = SubjectHelperMixin()
        self.subject_identifier = self.subject_helper_cls.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            child_dataset.study_child_identifier,
            version='3',
            child_version='3',
            options=self.options,
            child_consent_options=child_consent_options,
            update_created_dt=True)

        # Update onschedule datetime to reflect correct consent datetime
        self.a_onschedule = OnScheduleCohortAEnrollment.objects.get(
            subject_identifier=self.subject_identifier)
        self.a_onschedule.onschedule_datetime = self.options.get('consent_datetime')
        self.a_onschedule.save()


    def test_cohort_a_to_cohort_b_enrolment(self):
        subject_consent = SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier)

        child_consent = subject_consent.caregiverchildconsent_set.first()

        # Trigger caregiver quarterly schedule enrolment
        enrol_appt = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            schedule_name=self.a_onschedule.schedule_name)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=enrol_appt,
            report_datetime=enrol_appt.appt_datetime,
            reason=SCHEDULED)

        enrol_appt.appt_status = INCOMPLETE_APPT
        enrol_appt.save()

        self.assertTrue(OnScheduleCohortAQuarterly.objects.filter(
            subject_identifier=self.subject_identifier,
            child_subject_identifier=child_consent.subject_identifier).exists())

        quart_appt = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            visit_code='2001M')

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=quart_appt,
            report_datetime=quart_appt.appt_datetime,
            reason=SCHEDULED)

        quart_appt.appt_status = INCOMPLETE_APPT
        quart_appt.save()

        # Trigger child quarterly schedule enrolment
        child_enrol_appt = ChildAppointment.objects.get(
            subject_identifier=child_consent.subject_identifier,
            visit_code='2000')

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=child_enrol_appt,
            report_datetime=child_enrol_appt.appt_datetime,
            reason=SCHEDULED)

        child_enrol_appt.appt_status = INCOMPLETE_APPT
        child_enrol_appt.save()

        self.assertTrue(OnScheduleChildCohortAQuarterly.objects.filter(
            subject_identifier=child_consent.subject_identifier).exists())

        child_quart_appt = ChildAppointment.objects.get(
            subject_identifier=child_consent.subject_identifier,
            visit_code='2001')

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=child_quart_appt,
            report_datetime=child_quart_appt.appt_datetime,
            reason=SCHEDULED)

        child_quart_appt.appt_status = INCOMPLETE_APPT
        child_quart_appt.save()

        sq_enrol_helper = SequentialCohortEnrollment(
            child_subject_identifier=child_consent.subject_identifier)

        sq_enrol_helper.age_up_enrollment()
    
        # Check participant offschedule for previous cohort
        self.assertTrue(CaregiverOffSchedule.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name=quart_appt.schedule_name).exists())

        self.assertTrue(ChildOffSchedule.objects.filter(
            subject_identifier=child_consent.subject_identifier,
            schedule_name=child_quart_appt.schedule_name).exists())

        b_onschedule = OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=self.subject_identifier)
        self.assertTrue(b_onschedule.exists())

        child_b_onsch = OnScheduleChildCohortBQuarterly.objects.filter(
            subject_identifier=child_consent.subject_identifier)
        self.assertTrue(child_b_onsch.exists())

        # Check appointments completed on previous cohort does not exist.
        appts = Appointment.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name=b_onschedule[0].schedule_name)
        self.assertFalse(appts.filter(visit_code='2001M').exists())

        child_appts = ChildAppointment.objects.filter(
            subject_identifier=child_consent.subject_identifier,
            schedule_name=child_b_onsch[0].schedule_name)
        self.assertFalse(child_appts.filter(visit_code='2001').exists())

    def test_cohort_b_to_cohort_c_enrollment(self):
        study_maternal_identifier = '11721'

        options = {
            'consent_datetime': get_utcnow() - relativedelta(years=1),
            'version': '3'}

        child_consent_options = {
            'consent_datetime': get_utcnow() - relativedelta(years=1)}

        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=10, months=1),
            'mom_enrolldate': get_utcnow() - relativedelta(years=10,  months=11),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': study_maternal_identifier,
            'protocol': 'Tshilo Dikotla',
            'mom_pregarv_strat': '3-drug ART'}

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **maternal_dataset_options)

        child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow() - relativedelta(years=10, months=11),
            'study_maternal_identifier': study_maternal_identifier,
            'study_child_identifier': '1143'}

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=1),
            **child_dataset_options)

        subject_identifier = self.subject_helper_cls.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            child_dataset.study_child_identifier,
            version='3',
            child_version='3',
            options=options,
            child_consent_options=child_consent_options,
            update_created_dt=True)

        # Update onschedule datetime to reflect correct consent datetime
        b_onschedule = OnScheduleCohortBEnrollment.objects.get(
            subject_identifier=subject_identifier)
        b_onschedule.onschedule_datetime = options.get('consent_datetime')
        b_onschedule.save()

        subject_consent = SubjectConsent.objects.get(
            subject_identifier=subject_identifier)

        child_consent = subject_consent.caregiverchildconsent_set.first()

        self.assertFalse(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            child_subject_identifier=child_consent.subject_identifier).exists())

        # Trigger caregiver quarterly schedule enrolment
        enrol_appt = Appointment.objects.get(
            subject_identifier=subject_identifier,
            schedule_name=b_onschedule.schedule_name)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=enrol_appt,
            report_datetime=enrol_appt.appt_datetime,
            reason=SCHEDULED)

        enrol_appt.appt_status = INCOMPLETE_APPT
        enrol_appt.save()

        self.assertTrue(OnScheduleCohortBQuarterly.objects.filter(
            subject_identifier=subject_identifier,
            child_subject_identifier=child_consent.subject_identifier).exists())

        quart_appt = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code='2001M')

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=quart_appt,
            report_datetime=quart_appt.appt_datetime,
            reason=SCHEDULED)

        quart_appt.appt_status = INCOMPLETE_APPT
        quart_appt.save()

        # Confirm child schedules and appointments
        self.assertTrue(OnScheduleChildCohortBEnrollment.objects.filter(
            subject_identifier=child_consent.subject_identifier, ).exists())

        self.assertFalse(OnScheduleChildCohortBQuarterly.objects.filter(
            subject_identifier=child_consent.subject_identifier, ).exists())

        # Trigger child quarterly schedule enrolment
        child_enrol_appt = ChildAppointment.objects.get(
            subject_identifier=child_consent.subject_identifier,
            visit_code='2000')

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=child_enrol_appt,
            report_datetime=child_enrol_appt.appt_datetime,
            reason=SCHEDULED)

        child_enrol_appt.appt_status = INCOMPLETE_APPT
        child_enrol_appt.save()

        self.assertTrue(OnScheduleChildCohortBQuarterly.objects.filter(
            subject_identifier=child_consent.subject_identifier).exists())

        child_quart_appt = ChildAppointment.objects.get(
            subject_identifier=child_consent.subject_identifier,
            visit_code='2001')

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=child_quart_appt,
            report_datetime=child_quart_appt.appt_datetime,
            reason=SCHEDULED)

        child_quart_appt.appt_status = INCOMPLETE_APPT
        child_quart_appt.save()

        sq_enrol_helper = SequentialCohortEnrollment(
            child_subject_identifier=child_consent.subject_identifier)

        sq_enrol_helper.age_up_enrollment()

        # Check participant offschedule for previous cohort
        self.assertTrue(CaregiverOffSchedule.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name=quart_appt.schedule_name).exists())

        self.assertTrue(ChildOffSchedule.objects.filter(
            subject_identifier=child_consent.subject_identifier,
            schedule_name=child_quart_appt.schedule_name).exists())

        c_onschedule = OnScheduleCohortCQuarterly.objects.filter(
            subject_identifier=subject_identifier)
        self.assertTrue(c_onschedule.exists())

        c_fu = OnScheduleCohortCFUSeq.objects.filter(
            subject_identifier=subject_identifier)
        self.assertTrue(c_fu.exists())

        child_c_onsch = OnScheduleChildCohortCQuarterly.objects.filter(
            subject_identifier=child_consent.subject_identifier)
        self.assertTrue(child_c_onsch.exists())

        child_c_fu = OnScheduleChildCohortCFUSeq.objects.filter(
            subject_identifier=child_consent.subject_identifier)
        self.assertTrue(child_c_fu.exists())

        # Check appointments completed on previous cohort does not exist.
        appts = Appointment.objects.filter(
            subject_identifier=subject_identifier,
            schedule_name=c_onschedule[0].schedule_name)
        self.assertFalse(appts.filter(visit_code='2001M').exists())

        child_appts = ChildAppointment.objects.filter(
            subject_identifier=child_consent.subject_identifier,
            schedule_name=child_c_onsch[0].schedule_name)
        self.assertFalse(child_appts.filter(visit_code='2001').exists())


    def test_primary_sq_enrol_fu(self):
        subject_consent = SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier)

        child_consent = subject_consent.caregiverchildconsent_set.first()

        # Trigger caregiver quarterly schedule enrolment
        enrol_appt = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            schedule_name=self.a_onschedule.schedule_name)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=enrol_appt,
            report_datetime=enrol_appt.appt_datetime,
            reason=SCHEDULED)

        enrol_appt.appt_status = INCOMPLETE_APPT
        enrol_appt.save()

        quart_appt = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            visit_code='2001M')

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=quart_appt,
            report_datetime=quart_appt.appt_datetime,
            reason=SCHEDULED)

        quart_appt.appt_status = INCOMPLETE_APPT
        quart_appt.save()

        # Trigger child quarterly schedule enrolment
        child_enrol_appt = ChildAppointment.objects.get(
            subject_identifier=child_consent.subject_identifier,
            visit_code='2000')

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=child_enrol_appt,
            report_datetime=child_enrol_appt.appt_datetime,
            reason=SCHEDULED)

        child_enrol_appt.appt_status = INCOMPLETE_APPT
        child_enrol_appt.save()

        child_quart_appt = ChildAppointment.objects.get(
            subject_identifier=child_consent.subject_identifier,
            visit_code='2001')

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=child_quart_appt,
            report_datetime=child_quart_appt.appt_datetime,
            reason=SCHEDULED)

        child_quart_appt.appt_status = INCOMPLETE_APPT
        child_quart_appt.save()

        sq_enrol_helper = SequentialCohortEnrollment(
            child_subject_identifier=child_consent.subject_identifier)

        sq_enrol_helper.age_up_enrollment()

        b_fu = OnScheduleCohortBFUSeq.objects.filter(
            subject_identifier=self.subject_identifier)
        self.assertTrue(b_fu.exists())

        child_b_fu = OnScheduleChildCohortBFUSeq.objects.filter(
            subject_identifier=child_consent.subject_identifier)
        self.assertTrue(child_b_fu.exists())

        # Check FU appointments created.
        appts = Appointment.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name=b_fu[0].schedule_name)
        self.assertTrue(appts.exists())
        self.assertEqual(appts[0].visit_code, '3000B')

        child_appts = ChildAppointment.objects.filter(
            subject_identifier=child_consent.subject_identifier,
            schedule_name=child_b_fu[0].schedule_name)
        self.assertTrue(child_appts.exists())
        self.assertEqual(child_appts[0].visit_code, '3000B')

    def test_second_sq_enrol_fu(self):
        """ Assert participant already completed their initial FU and is
            sequentially enrolled for second FU is enrolled correctly on the
            sequential FU schedules. i.e. 3000[A|B|C {for cohort variable}].
        """
        subject_consent = SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier)

        child_consent = subject_consent.caregiverchildconsent_set.first()

        # Trigger caregiver quarterly schedule enrolment
        enrol_appt = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            schedule_name=self.a_onschedule.schedule_name)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=enrol_appt,
            report_datetime=enrol_appt.appt_datetime,
            reason=SCHEDULED)

        enrol_appt.appt_status = INCOMPLETE_APPT
        enrol_appt.save()

        quart_appt = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            visit_code='2001M')

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=quart_appt,
            report_datetime=quart_appt.appt_datetime,
            reason=SCHEDULED)

        quart_appt.appt_status = INCOMPLETE_APPT
        quart_appt.save()

        # Trigger child quarterly schedule enrolment
        child_enrol_appt = ChildAppointment.objects.get(
            subject_identifier=child_consent.subject_identifier,
            visit_code='2000')

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=child_enrol_appt,
            report_datetime=child_enrol_appt.appt_datetime,
            reason=SCHEDULED)

        child_enrol_appt.appt_status = INCOMPLETE_APPT
        child_enrol_appt.save()

        child_quart_appt = ChildAppointment.objects.get(
            subject_identifier=child_consent.subject_identifier,
            visit_code='2001')

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=child_quart_appt,
            report_datetime=child_quart_appt.appt_datetime,
            reason=SCHEDULED)

        child_quart_appt.appt_status = INCOMPLETE_APPT
        child_quart_appt.save()

        # Enrol on FU schedule
        fu_enrol_helper = ChildFollowUpEnrolmentHelper(
            subject_identifier=child_consent.subject_identifier)
        fu_enrol_helper.activate_child_fu_schedule()

        a_fu = OnScheduleCohortAFU.objects.filter(
            subject_identifier=self.subject_identifier)
        a_fu_appts = Appointment.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name=a_fu[0].schedule_name)
        self.assertTrue(a_fu.exists())
        self.assertEqual(a_fu_appts[0].visit_code, '3000M')

        child_a_fu = OnScheduleChildCohortAFU.objects.filter(
            subject_identifier=child_consent.subject_identifier)
        child_a_fu_appts = ChildAppointment.objects.filter(
            subject_identifier=child_consent.subject_identifier,
            schedule_name=child_a_fu[0].schedule_name)
        self.assertTrue(child_a_fu.exists())
        self.assertEqual(child_a_fu_appts[0].visit_code, '3000')

        sq_enrol_helper = SequentialCohortEnrollment(
            child_subject_identifier=child_consent.subject_identifier)

        sq_enrol_helper.age_up_enrollment()

        b_sq_fu = OnScheduleCohortBFUSeq.objects.filter(
            subject_identifier=self.subject_identifier)
        self.assertTrue(b_sq_fu.exists())

        child_b_sq_fu = OnScheduleChildCohortBFUSeq.objects.filter(
            subject_identifier=child_consent.subject_identifier)
        self.assertTrue(child_b_sq_fu.exists())

        # Check FU appointments created.
        appts = Appointment.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name=b_sq_fu[0].schedule_name)
        self.assertTrue(appts.exists())
        self.assertEqual(appts[0].visit_code, '3000B')

        child_appts = ChildAppointment.objects.filter(
            subject_identifier=child_consent.subject_identifier,
            schedule_name=child_b_sq_fu[0].schedule_name)
        self.assertTrue(child_appts.exists())
        self.assertEqual(child_appts[0].visit_code, '3000B')


    def test_primary_to_sec_fu_sq_caregiver(self):
        """ Assert participant already completed FU from their previous cohort schedules,
            and is sequentially enrolled to secondary aims continues quarterly appts on
            secondary aims FU sequential schedule. i.e. 3001S, 3002S etc.
        """
        subject_consent = SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier)

        child_consent = subject_consent.caregiverchildconsent_set.first()

        # Trigger caregiver quarterly schedule enrolment
        enrol_appt = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            schedule_name=self.a_onschedule.schedule_name)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=enrol_appt,
            report_datetime=enrol_appt.appt_datetime,
            reason=SCHEDULED)

        enrol_appt.appt_status = INCOMPLETE_APPT
        enrol_appt.save()

        quart_appt = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            visit_code='2001M')

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=quart_appt,
            report_datetime=quart_appt.appt_datetime,
            reason=SCHEDULED)

        quart_appt.appt_status = INCOMPLETE_APPT
        quart_appt.save()

        # Trigger child quarterly schedule enrolment
        child_enrol_appt = ChildAppointment.objects.get(
            subject_identifier=child_consent.subject_identifier,
            visit_code='2000')

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=child_enrol_appt,
            report_datetime=child_enrol_appt.appt_datetime,
            reason=SCHEDULED)

        child_enrol_appt.appt_status = INCOMPLETE_APPT
        child_enrol_appt.save()

        child_quart_appt = ChildAppointment.objects.get(
            subject_identifier=child_consent.subject_identifier,
            visit_code='2001')

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=child_quart_appt,
            report_datetime=child_quart_appt.appt_datetime,
            reason=SCHEDULED)

        child_quart_appt.appt_status = INCOMPLETE_APPT
        child_quart_appt.save()

        # Enrol on FU schedule
        fu_enrol_helper = ChildFollowUpEnrolmentHelper(
            subject_identifier=child_consent.subject_identifier)
        fu_enrol_helper.activate_child_fu_schedule()

        a_fu = OnScheduleCohortAFU.objects.filter(
            subject_identifier=self.subject_identifier)
        a_fu_appts = Appointment.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name=a_fu[0].schedule_name)


        child_a_fu = OnScheduleChildCohortAFU.objects.filter(
            subject_identifier=child_consent.subject_identifier)
        child_a_fu_appts = ChildAppointment.objects.filter(
            subject_identifier=child_consent.subject_identifier,
            schedule_name=child_a_fu[0].schedule_name)
 
        # Complete FU visit, to trigger FU quarterly
        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=a_fu_appts[0],
            report_datetime=a_fu_appts[0].appt_datetime,
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=child_a_fu_appts[0],
            report_datetime=child_a_fu_appts[0].appt_datetime,
            reason=SCHEDULED)

        # Update maternal dataset to enrol on secondary aims when aging up
        maternal_dataset = MaternalDataset.objects.filter(
            screening_identifier=subject_consent.screening_identifier)
        maternal_dataset.update(mom_pregarv_strat=None)

        sq_enrol_helper = SequentialCohortEnrollment(
            child_subject_identifier=child_consent.subject_identifier)

        sq_enrol_helper.age_up_enrollment()

        sec_fu_sq = OnScheduleCohortBSecSeq.objects.filter(
            subject_identifier=self.subject_identifier)
        self.assertTrue(sec_fu_sq.exists())
        sec_fu_appts = Appointment.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name=sec_fu_sq[0].schedule_name)
        self.assertTrue(sec_fu_appts[0].visit_code.endswith('S'))

        child_sec_fu_sq = OnScheduleChildCohortBSecSeq.objects.filter(
            subject_identifier=child_consent.subject_identifier,)
        self.assertTrue(child_sec_fu_sq.exists())
        child_sec_fu_appts = ChildAppointment.objects.filter(
            subject_identifier=child_consent.subject_identifier,
            schedule_name=child_sec_fu_sq[0].schedule_name)
        self.assertTrue(child_sec_fu_appts[0].visit_code.endswith('S'))
