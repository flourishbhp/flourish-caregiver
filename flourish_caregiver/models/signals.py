import os

import pytz
import PIL
import pyminizip
import pypdfium2 as pdfium
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.db.transaction import TransactionManagementError
from django.dispatch import receiver
from edc_action_item import site_action_items
from edc_base.utils import age, get_utcnow
from edc_constants.constants import NEW, NO, OPEN
from edc_constants.constants import YES
from edc_data_manager.models import DataActionItem
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import MISSED_VISIT, LOST_VISIT
from edc_appointment.constants import COMPLETE_APPT
from PIL import Image
from edc_appointment.models import Appointment
from flourish_prn.action_items import CAREGIVER_DEATH_REPORT_ACTION
from .antenatal_enrollment import AntenatalEnrollment
from .caregiver_child_consent import CaregiverChildConsent
from .caregiver_clinician_notes import ClinicianNotesImage
from .caregiver_locator import CaregiverLocator
from .caregiver_previously_enrolled import CaregiverPreviouslyEnrolled
from .cohort import Cohort
from .locator_logs import LocatorLog, LocatorLogEntry
from .maternal_dataset import MaternalDataset
from .maternal_delivery import MaternalDelivery
from .maternal_visit import MaternalVisit
from .subject_consent import SubjectConsent
from .tb_engagement import TbEngagement
from .tb_interview import TbInterview
from .tb_referral_outcomes import TbReferralOutcomes
from .ultrasound import UltraSound
from ..action_items import TB_OFF_STUDY_ACTION
from ..constants import MAX_GA_LMP_ENROL_WEEKS, MIN_GA_LMP_ENROL_WEEKS
from ..helper_classes.auto_complete_child_crfs import AutoCompleteChildCrfs
from ..helper_classes.consent_helper import consent_helper
from ..helper_classes.fu_onschedule_helper import FollowUpEnrolmentHelper
from ..helper_classes.onschedule_helper import OnScheduleHelper
from ..helper_classes.utils import (cohort_assigned, update_preg_screening_obj_child_pid,
                                    get_related_child_count, get_child_consents,
                                    pf_identifier_check, create_unscheduled_appointment,
                                    create_call_reminder)
from ..models import CaregiverOffSchedule, ScreeningPregWomen
from ..models import ScreeningPriorBhpParticipants
from ..models.tb_informed_consent import TbInformedConsent
from ..models.tb_off_study import TbOffStudy  # was supposed to be in the prns
from ..models.tb_visit_screening_women import TbVisitScreeningWomen
from ..models.caregiver_tb_screening import CaregiverTBScreening

caregiver_config = django_apps.get_app_config('flourish_caregiver')


class PreFlourishError(Exception):
    pass


class ChildDatasetError(Exception):
    pass


class SubjectConsentError(Exception):
    pass


def update_maternal_dataset_and_worklist(subject_identifier,
                                         screening_identifier=None,
                                         study_child_identifier=None, ):
    study_maternal_identifier = None

    if study_child_identifier:
        child_dataset_cls = django_apps.get_model(
            'flourish_child.childdataset')
        try:
            child_dataset_obj = child_dataset_cls.objects.get(
                study_child_identifier=study_child_identifier)
        except child_dataset_cls.DoesNotExist:
            pass
        else:
            study_maternal_identifier = child_dataset_obj.study_maternal_identifier

    if screening_identifier or study_maternal_identifier:
        maternal_dataset_q = MaternalDataset.objects.filter(
            Q(screening_identifier=screening_identifier) |
            Q(study_maternal_identifier=study_maternal_identifier))

        if maternal_dataset_q:
            worklist_cls = django_apps.get_model('flourish_follow.worklist')
            maternal_dataset = maternal_dataset_q[0]

            if not maternal_dataset.subject_identifier:
                maternal_dataset.subject_identifier = subject_identifier
                maternal_dataset.save()

            study_maternal_identifier = maternal_dataset.study_maternal_identifier
            try:
                worklist = worklist_cls.objects.get(
                    study_maternal_identifier=study_maternal_identifier)
            except worklist_cls.DoesNotExist:
                pass
            else:
                worklist.consented = True
                worklist.assigned = None
                worklist.date_assigned = None
                worklist.save()

            screening_query_id = None
            if screening_identifier:
                screening_query_id = Q(
                    screening_identifier=screening_identifier)
            else:
                screening_query_id = Q(
                    study_maternal_identifier=study_maternal_identifier)

            try:
                screening_obj = ScreeningPriorBhpParticipants.objects.get(
                    screening_query_id)
            except ScreeningPriorBhpParticipants.DoesNotExist:
                pass
            else:
                screening_obj.subject_identifier = subject_identifier
                screening_obj.save_base(raw=True)


@receiver(post_save, weak=False, sender=CaregiverTBScreening,
          dispatch_uid='caregiver_tb_screening_on_post_save')
def caregiver_tb_screening_on_post_save(
        sender, instance, raw, created, **kwargs):

    if not raw:
        report_dt = instance.report_datetime
        visit_date = instance.clinic_visit_date

        dt_30days = (report_dt - relativedelta(days=30)).date()
        within_30days = visit_date >= dt_30days if visit_date else None

        if not within_30days:
            appointment = instance.maternal_visit.appointment
            try:
                appointment.__class__.objects.get(
                    subject_identifier=appointment.subject_identifier,
                    visit_code=appointment.visit_code,
                    visit_code_sequence=1,
                    schedule_name=appointment.schedule_name)
            except appointment.__class__.DoesNotExist:
                if (appointment.visit_code_sequence == 0 and instance.symptomatic and
                        not instance.tb_diagnoses):
                    scheduled_dt = report_dt + relativedelta(weeks=2)
                    scheduled_dt = scheduled_dt.astimezone(
                        pytz.timezone('Africa/Gaborone'))
                    _appt = create_unscheduled_appointment(
                        appointment, scheduled_dt)
                    if _appt:
                        # Update the appointment date time to reflect correctly.
                        _appt.appt_datetime = scheduled_dt
                        _appt.save()
                        title = (f'{appointment.subject_identifier[-6:]}'
                                 f' TB 2 week call : @ {appointment.visit_code}')
                        reminder_time = time(8, 0)
                        repeat = 'once'
                        create_call_reminder(title, scheduled_dt.date(), reminder_time,
                                             repeat)


@receiver(post_save, weak=False, sender=SubjectConsent,
          dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """ Update subject identifier after consent.
    """
    if not raw:
        update_maternal_dataset_and_worklist(
            instance.subject_identifier,
            screening_identifier=instance.screening_identifier)

        # Update subject identifier on the screening obj when created

        try:
            screening_obj = ScreeningPregWomen.objects.get(
                screening_identifier=instance.screening_identifier)
        except ScreeningPregWomen.DoesNotExist:
            pass
        else:
            screening_obj.subject_identifier = instance.subject_identifier
            screening_obj.save_base(raw=True)


@receiver(post_save, weak=False, sender=LocatorLogEntry,
          dispatch_uid='locator_log_entry_on_post_save')
def locator_log_entry_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Create locator log entry
    """
    if not raw:
        if created:
            try:
                locator_group = Group.objects.get(name='locator users')
            except Group.DoesNotExist:
                locator_group = Group.objects.create(name='locator users')
            if not User.objects.filter(username=instance.user_created,
                                       groups__name='locator users').exists():
                try:
                    user = User.objects.get(username=instance.user_created)
                except User.DoesNotExist:
                    raise ValueError(
                        f'The user {instance.user_created}, does not exist.')
                else:
                    locator_group.user_set.add(user)


@receiver(post_save, weak=False, sender=MaternalDataset,
          dispatch_uid='maternal_dataset_on_post_save')
def maternal_dataset_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Create locator log entry
    """
    if not raw:
        if created:
            try:
                LocatorLog.objects.get(maternal_dataset=instance)
            except LocatorLog.DoesNotExist:
                LocatorLog.objects.create(maternal_dataset=instance)


@receiver(post_save, weak=False, sender=CaregiverLocator,
          dispatch_uid='caregiver_locator_on_post_save')
def caregiver_locator_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Create locator log entry
    """

    '''
    Check if the participant exist in the maternal dataset without
     using a try catch block for performance reason
    '''
    maternal_data = MaternalDataset.objects.filter(
        screening_identifier=instance.screening_identifier)

    if maternal_data.exists():

        maternal_data_details = maternal_data.first()

        '''
        If firstname or lastname defers update the maternal dataset
        '''
        if maternal_data_details.first_name != instance.first_name \
                or maternal_data_details.last_name != instance.last_name:
            maternal_data_details.first_name = instance.first_name
            maternal_data_details.last_name = instance.last_name
            maternal_data_details.save()

    child_dataset_cls = django_apps.get_model('flourish_child.childdataset')
    if not raw:
        if created:
            try:
                maternal_dataset = MaternalDataset.objects.get(
                    study_maternal_identifier=instance.study_maternal_identifier)
            except MaternalDataset.DoesNotExist:
                pass
            else:
                offstudy_td = True
                if maternal_dataset.protocol == 'Tshilo Dikotla':
                    try:
                        child_dataset = child_dataset_cls.objects.get(
                            study_maternal_identifier=maternal_dataset
                            .study_maternal_identifier)
                    except child_dataset_cls.DoesNotExist:
                        raise
                    else:
                        offstudy_td = child_dataset.infant_offstudy_complete == 1

                if offstudy_td:
                    worklist_cls = django_apps.get_model(
                        'flourish_follow.worklist')
                    try:

                        worklist_cls.objects.get(
                            study_maternal_identifier=instance.study_maternal_identifier)
                    except worklist_cls.DoesNotExist:
                        worklist_cls.objects.create(
                            study_maternal_identifier=instance.study_maternal_identifier,
                            prev_study=maternal_dataset.protocol,
                            user_created=instance.user_created)


@receiver(post_save, weak=False, sender=AntenatalEnrollment,
          dispatch_uid='antenatal_enrollment_on_post_save')
def antenatal_enrollment_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put subject on cohort a schedule.
    """
    registered_subject_cls = django_apps.get_model(
        'edc_registration.registeredsubject')

    children_count = 1 + registered_subject_cls.objects.filter(
        relative_identifier=instance.subject_identifier
    ).exclude(Q(subject_identifier=instance.child_subject_identifier) |
              Q(subject_identifier__endswith='-35') |
              Q(subject_identifier__endswith='-46') |
              Q(subject_identifier__endswith='-56')).count()

    if not raw and instance.is_eligible:
        helper_cls = onschedule_helper_cls(instance.subject_identifier, )
        helper_cls.put_on_schedule(
            'cohort_a_antenatal',
            instance=instance,
            child_subject_identifier=instance.child_subject_identifier,
            caregiver_visit_count=children_count,
            base_appt_datetime=instance.report_datetime.replace(microsecond=0))


@receiver(post_save, weak=False, sender=MaternalDelivery,
          dispatch_uid='maternal_delivery_on_post_save')
def maternal_delivery_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put newborn child on schedule
    """
    tb_informed_consent_cls = django_apps.get_model(
        'flourish_caregiver.tbinformedconsent')
    schedule_history_cls = django_apps.get_model(
        'edc_visit_schedule.subjectschedulehistory')

    child_consents = get_child_consents(instance.subject_identifier)

    preg_child_consent = child_consents.filter(
        preg_enroll=True,
        subject_identifier=instance.child_subject_identifier)

    if preg_child_consent.exists():
        if instance.live_infants_to_register == 1:
            helper_cls = onschedule_helper_cls(instance.subject_identifier, )
            caregiver_visit_count = preg_child_consent.latest(
                'consent_datetime').caregiver_visit_count
            if not raw and created:
                helper_cls.put_on_schedule(
                    'cohort_a_birth',
                    instance=instance,
                    child_subject_identifier=instance.child_subject_identifier,
                    base_appt_datetime=instance.delivery_datetime.replace(
                        microsecond=0),
                    caregiver_visit_count=caregiver_visit_count)
                create_registered_infant(instance)
                try:
                    tb_informed_consent_cls.objects.get(
                        subject_identifier=instance.subject_identifier)
                except tb_informed_consent_cls.DoesNotExist:
                    pass
                else:
                    helper_cls.put_on_schedule(
                        'cohort_a_tb_2_months',
                        instance=instance,
                        child_subject_identifier=instance.child_subject_identifier,
                        base_appt_datetime=instance.delivery_datetime.replace(microsecond=0),
                        caregiver_visit_count=caregiver_visit_count)
        elif instance.still_births == 1:
            onschedules = schedule_history_cls.objects.filter(
                subject_identifier=instance.subject_identifier)
            for onschedule in onschedules:
                if onschedule.schedule_status == 'offschedule':
                    continue
                onschedule_cls = django_apps.get_model(onschedule.onschedule_model)
                try:
                    onschedule_obj = onschedule_cls.objects.get(
                        subject_identifier=instance.subject_identifier,
                        child_subject_identifier=instance.child_subject_identifier)
                except onschedule_cls.DoesNotExist:
                    continue
                else:
                    _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                        onschedule_model=onschedule_obj._meta.label_lower,
                        name=onschedule_obj.schedule_name)

                    schedule.take_off_schedule(
                        subject_identifier=instance.subject_identifier,
                        offschedule_datetime=instance.report_datetime,
                        schedule_name=onschedule_obj.schedule_name)


@receiver(post_save, weak=False, sender=CaregiverPreviouslyEnrolled,
          dispatch_uid='caregiver_previously_enrolled_on_post_save')
def caregiver_previously_enrolled_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put subject with participation on schedule after consenting.
    """
    if not raw:
        child_assent_cls = django_apps.get_model('flourish_child.childassent')

        child_identifiers = CaregiverChildConsent.objects.filter(
            subject_consent__subject_identifier=instance.subject_identifier).values_list(
            'subject_identifier', flat=True).distinct()

        child_assents = child_assent_cls.objects.filter(
            subject_identifier__in=child_identifiers)

        for child in child_assents:
            child.save()

        assent_identifiers = child_assents.values_list(
            'subject_identifier', flat=True).distinct()
        consent_diff = set(child_identifiers) - set(assent_identifiers)

        child_consents = CaregiverChildConsent.objects.filter(
            subject_identifier__in=list(consent_diff))

        for child in child_consents:
            child.save()


@receiver(post_save, weak=False, sender=CaregiverChildConsent,
          dispatch_uid='caregiver_child_consent_on_post_save')
def caregiver_child_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put subject on cohort a schedule after consenting on behalf of child.
    """
    if not raw and instance.is_eligible:
        cohort_obj = None
        if not bool(instance.study_child_identifier):
            update_preg_screening_obj_child_pid(
                instance.subject_consent,
                instance.subject_identifier)

        child_dummy_consent_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')

        child_age = None
        children_count = instance.caregiver_visit_count
        if not children_count:
            children_count = 1 + get_related_child_count(
                subject_identifier=instance.subject_consent.subject_identifier,
                child_subject_identifier=instance.subject_identifier)

        if instance.child_dob:
            child_age = age(instance.child_dob, get_utcnow())

        # Check if the participant has been put into an enrolment cohort
        try:
            cohort_obj = Cohort.objects.get(
                subject_identifier=instance.subject_identifier,
                enrollment_cohort=True)
        except Cohort.DoesNotExist:
            cohort = cohort_assigned(instance.study_child_identifier,
                                     instance.child_dob,
                                     instance.subject_consent.consent_datetime.date())

            if not cohort and screening_preg_exists(instance):
                cohort = 'cohort_a'

            if child_age is not None and child_age.years < 7:
                try:
                    child_dummy_consent_cls.objects.get(
                        subject_identifier=instance.subject_identifier,
                        version=instance.version, )
                except child_dummy_consent_cls.DoesNotExist:
                    child_dummy_consent_cls.objects.create(
                        subject_identifier=instance.subject_identifier,
                        consent_datetime=instance.consent_datetime,
                        identity=instance.identity,
                        dob=instance.child_dob,
                        version=instance.version,
                        relative_identifier=instance.subject_consent.subject_identifier,
                        cohort=cohort)
            # Put participant into a cohort

            cohort_obj = Cohort.objects.create(
                subject_identifier=instance.subject_identifier,
                name=cohort,
                enrollment_cohort=True)

            instance.cohort = cohort_obj.name
            instance.save_base(raw=True)

        else:
            # TO-DO: Update child cohort
            try:
                prev_enrolled_obj = CaregiverPreviouslyEnrolled.objects.get(
                    subject_identifier=instance.subject_consent.subject_identifier)
            except CaregiverPreviouslyEnrolled.DoesNotExist:
                pass
            else:
                if (child_age and
                        instance.subject_identifier[-3:] not in ['-35', '-46', '-56']):
                    helper_cls = onschedule_helper_cls(cohort=instance.cohort)
                    _identifier = instance.study_child_identifier or ''

                    if pf_identifier_check(_identifier):
                        helper_cls.put_on_fu_schedule(
                            instance,
                            instance.subject_identifier,
                            base_appt_datetime=instance.consent_datetime.replace(
                                microsecond=0),
                            child_count=children_count)
                    else:
                        helper_cls.put_cohort_onschedule(
                            instance,
                            base_appt_datetime=prev_enrolled_obj.report_datetime.replace(
                                microsecond=0))

            # Get or create a child dummy consent instance (account for
            # re-consenting).
            try:
                child_dummy_consent = child_dummy_consent_cls.objects.get(
                    subject_identifier=instance.subject_identifier,
                    version=instance.version, )
            except child_dummy_consent_cls.DoesNotExist:
                child_dummy_consent = child_dummy_consent_cls.objects.create(
                    subject_identifier=instance.subject_identifier,
                    consent_datetime=instance.consent_datetime,
                    identity=instance.identity,
                    dob=instance.child_dob,
                    version=instance.version,
                    relative_identifier=instance.subject_consent.subject_identifier,
                    cohort=instance.cohort)
            else:
                if not child_dummy_consent.cohort:
                    child_dummy_consent.cohort = instance.cohort
                child_dummy_consent.save()

        if created:
            instance.caregiver_visit_count = children_count
            instance.save_base(raw=True)

        if instance.study_child_identifier:
            update_maternal_dataset_and_worklist(
                instance.subject_consent.subject_identifier,
                screening_identifier=instance.subject_consent.screening_identifier,
                study_child_identifier=instance.study_child_identifier)

        # Resave cohort object to update enrolment variables, once participant
        # has been put on schedule.
        if cohort_obj:
            cohort_obj.save()


@receiver(post_save, weak=False, sender=ClinicianNotesImage,
          dispatch_uid='clinician_notes_image_on_post_save')
def clinician_notes_image_on_post_save(sender, instance, raw, created, **kwargs):
    """
    Ecrypt an image and add stamp before saving
    """
    if not raw and created:
        stamp_image(instance)


@receiver(post_save, weak=False, sender=MaternalVisit,
          dispatch_uid='maternal_visit_on_post_save')
def maternal_visit_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put subject on quarterly schedule at enrollment visit.
    """
    survival_status = instance.survival_status
    death_report_cls = django_apps.get_model(
        'flourish_prn.caregiverdeathreport')
    if survival_status == 'dead':
        trigger_action_item(death_report_cls,
                            CAREGIVER_DEATH_REPORT_ACTION,
                            instance.subject_identifier)

    if instance.brain_scan and instance.brain_scan == YES:
        """
        If the mother is interested in brain scan, a notification will be created
        so a crf can be completed on redcap
        """
        DataActionItem.objects.update_or_create(
            subject='Complete Infant Ultrasound Component on REDCAP',
            subject_identifier=instance.subject_identifier,
            assigned='clinic',
            comment='''\
                    Caregiver is interested in ultrasound brain scan for the infant,
                     please complete Infant Ultrasound Component on REDCAP
                    '''
        )

    """
    trigger off schedule for participants who missed a TB visit
    """
    tb_off_study_cls = django_apps.get_model(
        'flourish_caregiver.tboffstudy'
    )
    if instance.visit_code in ['2200T' '2100T'] and (instance.reason == MISSED_VISIT or
                                                     instance.reason == LOST_VISIT) :
        trigger_action_item(tb_off_study_cls,
                            TB_OFF_STUDY_ACTION,
                            instance.subject_identifier)

    if not raw and created and instance.visit_code in ['2000M', '2000D', '3000M',
                                                       '3000A', '3000B', '3000C']:
        base_appt_datetime = instance.report_datetime.replace(microsecond=0)
        helper_cls = onschedule_helper_cls(instance.subject_identifier, )
        helper_cls.put_quarterly_onschedule(
            instance, base_appt_datetime=base_appt_datetime)

    """
    For parents with two kids, crfs collected on a visit of one kid are being
      when opening such crf
    """
    complete_child_crfs = AutoCompleteChildCrfs(instance=instance)
    try:
        complete_child_crfs.pre_fill_crfs()
    except TransactionManagementError:
        """
        Ignore the all errors and do not create any objects (Ostrich algorithm).
        Nothing will be affected
        """
        pass

@receiver(post_save, weak=False, sender=Appointment,
          dispatch_uid='tb_six_month_appointment_on_post_save')
def tb_six_month_appointment_on_post_save(sender, instance, raw, created, **kwargs):

    tb_off_study_cls = django_apps.get_model(
        'flourish_caregiver.tboffstudy'
    )
    if  instance.visit_code == '2200T' and instance.appt_status == COMPLETE_APPT:
        trigger_action_item(tb_off_study_cls,TB_OFF_STUDY_ACTION,
                            instance.subject_identifier)


@receiver(post_save, weak=False, sender=TbVisitScreeningWomen,
          dispatch_uid='tb_visit_screening_women_post_save')
def tb_visit_screening_women_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        tb_off_study_cls = django_apps.get_model(
            'flourish_caregiver.tboffstudy')

        tb_referral = (
            instance.have_cough == YES or
            instance.cough_duration == '=>2 week' or
            instance.fever == YES or
            instance.night_sweats == YES or
            instance.weight_loss == YES or
            instance.cough_blood == YES or
            instance.enlarged_lymph_nodes == YES
        )

        if not tb_referral:
            trigger_action_item(tb_off_study_cls,
                                TB_OFF_STUDY_ACTION,
                                instance.subject_identifier)
        else:
            try:
                child_consent = CaregiverChildConsent.objects.filter(
                    subject_consent__subject_identifier=instance.subject_identifier,
                    preg_enroll=True).latest('consent_datetime')
            except CaregiverChildConsent.DoesNotExist:
                pass
            else:
                onschedule_dt = instance.report_datetime.replace(microsecond=0)
                helper_cls = onschedule_helper_cls(instance.subject_identifier, )

                helper_cls.put_on_schedule(
                    'cohort_a_tb_6_months',
                    instance=instance,
                    child_subject_identifier=child_consent.subject_identifier,
                    base_appt_datetime=onschedule_dt,
                    caregiver_visit_count=child_consent.caregiver_visit_count)


@receiver(post_save, weak=False, sender=TbOffStudy,
          dispatch_uid='tb_offstudy_post_save')
def tb_offstudy_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        tb_onschedules = {
            'flourish_caregiver.onschedulecohortatb2months': ['a_tb1_2_months_schedule1',
                                                              'a_tb2_2_months_schedule1',
                                                              'a_tb3_2_months_schedule1'],
            'flourish_caregiver.onschedulecohortatb6months': ['a_tb1_6_months_schedule1',
                                                              'a_tb2_6_months_schedule1',
                                                              'a_tb3_6_months_schedule1']
        }

        for tb_onschedule, tb_schedules in tb_onschedules.items():
            for tb_schedule in tb_schedules:
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=tb_onschedule,
                    name=tb_schedule)
                if schedule.is_onschedule(subject_identifier=instance.subject_identifier,
                                          report_datetime=instance.report_datetime):
                    schedule.take_off_schedule(
                        subject_identifier=instance.subject_identifier,
                        schedule_name=tb_schedule)


@receiver(post_save, weak=False, sender=CaregiverOffSchedule,
          dispatch_uid='caregiver_off_schedule_on_post_save')
def maternal_caregiver_take_off_schedule(sender, instance, raw, created, **kwargs):
    for visit_schedule in site_visit_schedules.visit_schedules.values():
        for schedule in visit_schedule.schedules.values():
            onschedule_model_obj = get_onschedule_model_obj(
                schedule, instance.subject_identifier, instance.schedule_name)
            if (onschedule_model_obj
                    and onschedule_model_obj.schedule_name == instance.schedule_name):
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=onschedule_model_obj._meta.label_lower,
                    name=instance.schedule_name)
                if schedule.is_onschedule(
                        subject_identifier=instance.subject_identifier,
                        report_datetime=get_utcnow()):
                    schedule.take_off_schedule(
                        subject_identifier=instance.subject_identifier,
                        offschedule_datetime=instance.offschedule_datetime,
                        schedule_name=instance.schedule_name)
                # Remove remaining last appointment, future by upper window
                # period datetime.
                helper_cls = FollowUpEnrolmentHelper(
                    subject_identifier=instance.subject_identifier)
                helper_cls.delete_new_appt_window_after_date(
                    instance.offschedule_datetime,
                    visit_schedule_name=schedule._subject.visit_schedule_name,
                    schedule_name=instance.schedule_name)


@receiver(post_save, weak=False, sender=UltraSound,
          dispatch_uid='ultrasound_on_post_save')
def ultrasound_on_post_save(sender, instance, raw, created, **kwargs):
    """ Triggers caregiver offschedule, to remove mother on child related schedules.
        This is to account for multiple enrolment, can not take caregiver/mother
        offstudy.
        If only child, caregiver offstudy is handled on the dashboard to avoid overlapping.
    """
    if (instance.ga_confirmed_after < MIN_GA_LMP_ENROL_WEEKS
            or instance.ga_confirmed_after > MAX_GA_LMP_ENROL_WEEKS):
        child_count = get_related_child_count(
            subject_identifier=instance.subject_identifier,
            child_subject_identifier=instance.child_subject_identifier)

        if child_count >= 1:
            helper_cls = onschedule_helper_cls(
                subject_identifier=instance.subject_identifier, )
            helper_cls.create_caregiver_offschedule(
                instance.maternal_visit.schedule_name,
                offschedule_datetime=instance.report_datetime)


@receiver(post_save, weak=False, sender=ScreeningPregWomen,
          dispatch_uid='screening_preg_women_on_post_save')
def screening_preg_women(sender, instance, raw, created, **kwargs):
    if not raw:
        subject_consents = SubjectConsent.objects.filter(
            screening_identifier=instance.screening_identifier)

        if not subject_consents:
            create_consent_version(instance, version=caregiver_config.consent_version)


@receiver(post_save, weak=False, sender=ScreeningPriorBhpParticipants,
          dispatch_uid='screening_prior_bhp_participants_on_post_save')
def screening_prior_bhp_participants(sender, instance, raw, created, **kwargs):
    if not raw:

        subject_consents = SubjectConsent.objects.filter(
            screening_identifier=instance.screening_identifier)

        if not subject_consents:
            create_consent_version(instance, version=caregiver_config.consent_version)


@receiver(post_save, weak=False, sender=TbInformedConsent,
          dispatch_uid='tb_informed_consent_post_save')
def tb_informed_consent_post_save(sender, instance, raw, created, **kwargs):
    """
    Put subject on TB enrollment schedule after TB informed consent
    """
    maternal_delivery_cls = django_apps.get_model(
        'flourish_caregiver.maternaldelivery')
    if not raw:
        try:
            maternal_delivery_obj = maternal_delivery_cls.objects.get(
                subject_identifier=instance.subject_identifier)
        except maternal_delivery_cls.DoesNotExist:
            pass
        else:
            maternal_delivery_obj.save_base(raw=True)


@receiver(post_save, weak=False, sender=TbEngagement,
          dispatch_uid='tb_engagement_post_save')
def tb_engagement_post_save(sender, instance, raw, created, **kwargs):
    """
    Trigger offstudy if interview consent in NO
    """

    tb_off_study_cls = django_apps.get_model('flourish_caregiver.tboffstudy')

    trigger_action_item(tb_off_study_cls,
                        TB_OFF_STUDY_ACTION,
                        instance.subject_identifier,
                        opt_trigger=instance.interview_consent == NO)


@receiver(post_save, weak=False, sender=TbReferralOutcomes,
          dispatch_uid='tb_referral_outcomes_post_save')
def tb_referral_outcomes_post_save(sender, instance, raw, created, **kwargs):
    """
    Trigger offstudy if interview consent in NO
    """

    tb_off_study_cls = django_apps.get_model('flourish_caregiver.tboffstudy')

    trigger_action_item(tb_off_study_cls,
                        TB_OFF_STUDY_ACTION,
                        instance.subject_identifier,
                        opt_trigger=(instance.tb_eval == NO
                                     or instance.tb_treat_start == YES))


@receiver(post_save, weak=False, sender=TbInterview,
          dispatch_uid='tb_interview_post_save')
def tb_interview_post_save(sender, instance, raw, created, **kwargs):
    """
    Trigger offstudy if TB 6 month interview form is complete
    """

    tb_off_study_cls = django_apps.get_model('flourish_caregiver.tboffstudy')

    trigger_action_item(tb_off_study_cls,
                        TB_OFF_STUDY_ACTION,
                        instance.subject_identifier,
                        opt_trigger=True)


@receiver(pre_save, dispatch_uid='requires_consent_on_pre_save')
def validate_requires_consent_on_pre_save(instance, raw, **kwargs):
    """
    Validate that subject has consented to be in the study
    """
    if not raw:
        try:
            consent_model = site_visit_schedules.all_post_consent_models[
                instance._meta.label_lower]
        except KeyError:
            pass
        else:
            visit_schedule = consent_helper.get_visit_schedule(instance)
            if visit_schedule and visit_schedule.schedules:
                schedule = visit_schedule.schedules.get(
                    instance.visit.schedule_name)
                if schedule:
                    requires_consent = consent_helper.get_requires_consent(
                        instance, consent_model, schedule=schedule)
                    instance.consent_version = requires_consent.version
            elif consent_model:
                requires_consent = consent_helper.get_requires_consent(
                    instance, consent_model)
                instance.consent_version = requires_consent.version
            else:
                consent_helper.verify_registered_subject(instance)


def screening_preg_exists(child_consent_obj):
    preg_women_screening_cls = django_apps.get_model(
        'flourish_caregiver.screeningpregwomen')

    try:
        preg_women_screening_cls.objects.get(
            screening_identifier=child_consent_obj.subject_consent.screening_identifier)
    except preg_women_screening_cls.DoesNotExist:
        return False
    else:
        return True


def onschedule_helper_cls(
        subject_identifier=None, onschedule_datetime=None, cohort=None):
    helper_cls = OnScheduleHelper(subject_identifier,
                                  onschedule_datetime=onschedule_datetime,
                                  cohort=cohort)
    return helper_cls


def get_onschedule_model_obj(schedule, subject_identifier, schedule_name):
    try:
        return schedule.onschedule_model_cls.objects.get(
            subject_identifier=subject_identifier, schedule_name=schedule_name)
    except ObjectDoesNotExist:
        return None


def create_registered_infant(instance):
    #  Create infant registered subject
    if (isinstance(instance, MaternalDelivery) and
            getattr(instance, 'live_infants_to_register', None) == 1):
        maternal_consent = SubjectConsent.objects.filter(
            subject_identifier=instance.subject_identifier
        ).order_by('version').last()

        ultrasound_exists = UltraSound.objects.filter(
            maternal_visit__subject_identifier=instance.subject_identifier,
            child_subject_identifier=instance.child_subject_identifier
        ).exists()

        if not ultrasound_exists:
            raise ValidationError(
                f'Maternal Ultrasound must exist for {instance.subject_identifier}')
        else:
            with transaction.atomic():
                caregiver_child_consent_cls = django_apps.get_model(
                    'flourish_caregiver.caregiverchildconsent')

                child_consent_objs = caregiver_child_consent_cls.objects.filter(
                    subject_identifier=instance.child_subject_identifier)

                if not child_consent_objs.exists():
                    # Create caregiver child consent
                    caregiver_child_consent_cls.objects.create(
                        subject_consent=maternal_consent,
                        child_dob=instance.delivery_datetime.date(),
                        consent_datetime=get_utcnow(),
                        is_eligible=True)
                else:
                    caregiver_child_consent_obj = child_consent_objs.latest(
                        'consent_datetime')
                    child_dummy_consent_cls = django_apps.get_model(
                        'flourish_child.childdummysubjectconsent')
                    try:
                        child_dummy_consent_cls.objects.get(
                            subject_identifier=caregiver_child_consent_obj.subject_identifier,
                            version=caregiver_child_consent_obj.version)
                    except child_dummy_consent_cls.DoesNotExist:
                        child_dummy_consent_cls.objects.create(
                            subject_identifier=caregiver_child_consent_obj.subject_identifier,
                            consent_datetime=caregiver_child_consent_obj.consent_datetime,
                            dob=caregiver_child_consent_obj.dob,
                            cohort=caregiver_child_consent_obj.cohort,
                            version=caregiver_child_consent_obj.version,
                            relative_identifier=caregiver_child_consent_obj.subject_consent.subject_identifier)


def trigger_action_item(model_cls, action_name, subject_identifier,
                        repeat=False, opt_trigger=True):
    action_cls = site_action_items.get(
        model_cls.action_name)
    action_item_model_cls = action_cls.action_item_model_cls()

    try:
        model_cls.objects.get(subject_identifier=subject_identifier)
    except model_cls.DoesNotExist:
        trigger = opt_trigger and True
    else:
        trigger = repeat

    if trigger:
        try:
            action_item_obj = action_item_model_cls.objects.get(
                subject_identifier=subject_identifier,
                action_type__name=action_name)
        except action_item_model_cls.DoesNotExist:
            action_cls = site_action_items.get(action_name)
            action_cls(subject_identifier=subject_identifier)
        else:
            action_item_obj.status = OPEN
            action_item_obj.save()
    else:
        try:
            action_item = action_item_model_cls.objects.get(
                Q(status=NEW) | Q(status=OPEN),
                subject_identifier=subject_identifier,
                action_type__name=action_name)
        except action_item_model_cls.DoesNotExist:
            pass
        else:
            action_item.delete()


def create_consent_version(instance, version):
    consent_version_cls = django_apps.get_model(
        'flourish_caregiver.flourishconsentversion')

    try:
        consent_version_cls.objects.get(
            screening_identifier=instance.screening_identifier)
    except consent_version_cls.DoesNotExist:
        consent_version = consent_version_cls(
            screening_identifier=instance.screening_identifier,
            version=version,
            child_version=caregiver_config.child_consent_version,
            user_created=instance.user_modified or instance.user_created,
            created=get_utcnow())
        consent_version.save()


def stamp_image(instance):
    filefield = instance.image
    filename = filefield.name  # gets the "normal" file name as it was uploaded
    storage = filefield.storage
    path = storage.path(filename)
    if '.pdf' not in path:
        base_image = Image.open(path)
        stamped_img = add_image_stamp(base_image=base_image)
        stamped_img.save(path)
    else:
        print_pdf(path)


def add_image_stamp(base_image=None, position=(25, 25), resize=(500, 500)):
    """
    Superimpose image of a stamp over copy of the base image
    @param base_image: dir to base image
    @param dont_save: boolean for not saving the image just converting
    @param position: pixels(w,h) to superimpose stamp at
    """
    stamp = Image.open('media/stamp/true-copy.png')
    if resize:
        stamp = stamp.resize(resize, PIL.Image.ANTIALIAS)

    width, height = base_image.size
    stamp_width, stamp_height = stamp.size

    # Determine the orientation of the base image before pasting the stamp
    if width < height:
        pos_width = round(width / 2) - round(stamp_width / 2)
        pos_height = height - stamp_height
        position = (pos_width, pos_height)
    elif width > height:
        stamp = stamp.rotate(90)
        pos_width = width - stamp_width
        pos_height = round(height / 2) - round(stamp_height / 2)
        position = (pos_width, pos_height)

    # paste stamp over image
    base_image.paste(stamp, position, mask=stamp)
    return base_image


def print_pdf(filepath):
    pdf = pdfium.PdfDocument(filepath)
    page_indices = [i for i in range(len(pdf))]
    renderer = pdf.render_to(
        pdfium.BitmapConv.pil_image,
        page_indices=page_indices,
        scale=300 / 72
    )
    stamped_pdf_images = []
    for image, index in zip(renderer, page_indices):
        stamped_pdf_images.append(add_image_stamp(base_image=image))
    first_img = stamped_pdf_images[0]
    first_img.save(filepath, save_all=True,
                   append_images=stamped_pdf_images[1:])


def encrypt_files(instance, subject_identifier):
    base_path = settings.MEDIA_ROOT
    if instance.image:
        upload_to = f'{instance.image.field.upload_to}'
        timestamp = datetime.timestamp(get_utcnow())
        zip_filename = f'{subject_identifier}_{timestamp}.zip'
        with open('filekey.key', 'r') as filekey:
            key = filekey.read().rstrip()
        com_lvl = 8
        pyminizip.compress(f'{instance.image.path}', None,
                           f'{base_path}/{upload_to}{zip_filename}', key, com_lvl)
    # remove unencrypted file
    if os.path.exists(f'{instance.image.path}'):
        os.remove(f'{instance.image.path}')
    instance.image = f'{upload_to}{zip_filename}'
    instance.save()
