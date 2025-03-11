import re
import datetime

from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from edc_appointment.constants import NEW_APPT
from edc_appointment.creators import InvalidParentAppointmentMissingVisitError
from edc_appointment.creators import InvalidParentAppointmentStatusError
from edc_appointment.creators import UnscheduledAppointmentError

from ..helper_classes.unscheduled_appointment_creator import UnscheduledAppointmentCreator
from ..helper_classes.cohort_assignment import CohortAssignment


def cohort_assigned(study_child_identifier, child_dob, enrollment_date):
    """Calculates participant's cohort based on the maternal and child dataset
    """

    maternal_dataset_cls = django_apps.get_model('flourish_caregiver.maternaldataset')
    infant_dataset_cls = django_apps.get_model('flourish_child.childdataset')
    infant_dataset_obj = None
    try:
        infant_dataset_obj = infant_dataset_cls.objects.get(
            study_child_identifier=study_child_identifier,
            dob=child_dob)
    except infant_dataset_cls.DoesNotExist:
        pass
    except infant_dataset_cls.MultipleObjectsReturned:
        infant_dataset_obj = infant_dataset_cls.objects.filter(
            study_child_identifier=study_child_identifier,
            dob=child_dob)[0]
    finally:
        try:
            maternal_dataset_obj = maternal_dataset_cls.objects.get(
                study_maternal_identifier=getattr(
                    infant_dataset_obj, 'study_maternal_identifier', None))
        except maternal_dataset_cls.DoesNotExist:
            return None
        else:
            cohort = CohortAssignment(
                child_dob=child_dob,
                enrolment_dt=enrollment_date,
                child_hiv_exposure=getattr(
                    infant_dataset_obj, 'infant_hiv_exposed', None),
                arv_regimen=getattr(
                    maternal_dataset_obj, 'mom_pregarv_strat', None), )
            return cohort.cohort_variable or None


def update_preg_screening_obj_child_pid(consent, child_subject_identifier):
    screening_model_cls = django_apps.get_model('flourish_caregiver.screeningpregwomen')
    screening_obj = screening_model_cls.objects.filter(
        screening_identifier=consent.screening_identifier).first()

    if screening_obj:
        try:
            screening_obj.screeningpregwomeninline_set.get(
                child_subject_identifier=child_subject_identifier)
        except ObjectDoesNotExist:
            screenings_without_child_pid = (
                screening_obj.screeningpregwomeninline_set.filter(
                    Q(child_subject_identifier__isnull=True) | Q(
                        child_subject_identifier='')))
            if screenings_without_child_pid.count() == 1:
                child_screening_obj = screenings_without_child_pid.first()
                child_screening_obj.child_subject_identifier = child_subject_identifier
                child_screening_obj.save()
            elif screenings_without_child_pid.count() > 1:
                raise ValueError('More than one screening without child subject '
                                 'identifier found.')


def get_maternal_visit_by_id(visit_id=''):
    """ Returns the maternal visit instance for a specific id. """
    maternal_visit_cls = django_apps.get_model(
        'flourish_caregiver.maternalvisit')
    try:
        return maternal_visit_cls.objects.get(
            id=visit_id)
    except maternal_visit_cls.DoesNotExist:
        return None


def get_child_subject_identifier_by_visit(visit):
    """Returns the child subject identifier by visit."""
    schedule = getattr(visit, 'schedule', None)
    onschedule_model = getattr(schedule, 'onschedule_model', None)
    cohort_schedule_cls = django_apps.get_model(
        'flourish_caregiver.cohortschedules')

    if not onschedule_model:
        try:
            cohort_schedule = cohort_schedule_cls.objects.get(
                schedule_name=visit.schedule_name)
        except cohort_schedule_cls.DoesNotExist:
            pass
        else:
            onschedule_model = cohort_schedule.onschedule_model

    if onschedule_model:
        onschedule_model_cls = django_apps.get_model(onschedule_model)
        try:
            onschedule_obj = onschedule_model_cls.objects.get(
                subject_identifier=visit.subject_identifier,
                schedule_name=visit.schedule_name)
        except onschedule_model_cls.DoesNotExist:
            return None
        else:
            return onschedule_obj.child_subject_identifier


def get_schedule_names(instance):
    """ Returns schedule names for the specific related child
        @param instance: caregiver visit model instance
    """

    child_subject_identifier = get_child_subject_identifier_by_visit(instance)

    onschedules = get_child_related_schedules(
        instance.subject_identifier, child_subject_identifier)
    schedule_names = [onschedule.schedule_name for onschedule in onschedules]

    return schedule_names


def get_child_related_schedules(subject_identifier, child_subject_identifier):
    onschedules = []
    subject_schedule_history_model = 'edc_visit_schedule.subjectschedulehistory'
    subject_schedule_history_cls = django_apps.get_model(
        subject_schedule_history_model)

    qs = subject_schedule_history_cls.objects.filter(
        subject_identifier=subject_identifier).exclude(
        Q(schedule_name__icontains='tb') | Q(
            schedule_name__icontains='facet'))

    for model_obj in qs:
        onschedule_model_cls = django_apps.get_model(
            model_obj.onschedule_model)
        try:
            onschedule_model_cls.objects.get(
                subject_identifier=subject_identifier,
                child_subject_identifier=child_subject_identifier)
        except onschedule_model_cls.DoesNotExist:
            continue
        else:
            onschedules.append(model_obj)
    return onschedules


def get_previous_by_appt_datetime(appointment):
    schedule_names = get_schedule_names(appointment)
    try:
        previous_appt = appointment.__class__.objects.filter(
            subject_identifier=appointment.subject_identifier,
            appt_datetime__lt=appointment.appt_datetime,
            schedule_name__in=schedule_names,
            visit_code_sequence=0).latest('appt_datetime')
    except appointment.__class__.DoesNotExist:
        return None
    else:
        return previous_appt


def validate_date_not_in_past(value):
    if isinstance(value, datetime.date):
        value = datetime.datetime.combine(value, datetime.datetime.min.time())
    if value.date() < timezone.now().date():
        raise ValidationError(_('Invalid datetime - Can not be past date'),
                              code='creation_in_past')


def set_initials(first_name=None, last_name=None):
    initials = ''
    if first_name and last_name:
        if (len(first_name.split(' ')) > 1):
            first = first_name.split(' ')[0]
            middle = first_name.split(' ')[1]
            initials = f'{first[:1]}{middle[:1]}{last_name[:1]}'
        else:
            initials = f'{first_name[:1]}{last_name[:1]}'
    return initials


def get_pre_flourish_consent(screening_identifier):
    pf_consent_cls = django_apps.get_model('pre_flourish.preflourishconsent')
    try:
        pf_consent_obj = pf_consent_cls.objects.filter(
            screening_identifier=screening_identifier).latest('consent_datetime')
    except pf_consent_cls.DoesNotExist:
        return None
    else:
        return pf_consent_obj


def get_related_child_count(subject_identifier, child_subject_identifier):
    """ Return total number of children associated to the specific subject_identifier
        excluding the current `child_subject_identifier` provided.
        @param subject_identifier: parent participant identifier
        @param child_subject_identifier: child participant
        @return: total count of related children
    """
    registered_subject_cls = django_apps.get_model('edc_registration.registeredsubject')
    return registered_subject_cls.objects.filter(
        relative_identifier=subject_identifier).exclude(
        subject_identifier=child_subject_identifier, ).count()


def get_child_consents(subject_identifier):
    child_consent_cls = django_apps.get_model(
        'flourish_caregiver.caregiverchildconsent')

    return child_consent_cls.objects.filter(
        subject_consent__subject_identifier=subject_identifier).order_by(
        '-consent_datetime')


def get_locator_model_obj(subject_identifier):
    locator_model_cls = django_apps.get_model(
        'flourish_caregiver.caregiverlocator')
    try:
        return locator_model_cls.objects.get(
            subject_identifier=subject_identifier
        )
    except locator_model_cls.DoesNotExist:
        return None


def get_registration_date(subject_identifier, child_subject_identifier):
    """ Get date and time child was consented or registered to the study.
    """
    child_consents = get_child_consents(subject_identifier).filter(
        subject_identifier=child_subject_identifier, )

    if not child_consents.exists():
        raise forms.ValidationError(
            'Missing matching Child Subject Consent form, cannot proceed.')
    else:
        earliest_consent = child_consents.earliest('consent_datetime')
        return earliest_consent.consent_datetime


def pf_identifier_check(identifier):
    pattern = r'[B|C]142\-0[0-9A-Z]{8}\-[0-9]{1}P-[0-9]+'
    if re.fullmatch(pattern, identifier):
        return True
    else:
        return False


def create_unscheduled_appointment(appointment, reference_date):
    unscheduled_appointment_cls = UnscheduledAppointmentCreator

    options = {'subject_identifier': appointment.subject_identifier,
               'visit_schedule_name': appointment.visit_schedule_name,
               'schedule_name': appointment.schedule_name,
               'visit_code': appointment.visit_code,
               'facility': appointment.facility,
               'suggested_datetime': reference_date,
               'timepoint_datetime': reference_date,
               'check_appointment': False,
               'appt_status': NEW_APPT, }

    try:
        _appointment = unscheduled_appointment_cls(**options)
    except (ObjectDoesNotExist, UnscheduledAppointmentError,
            InvalidParentAppointmentMissingVisitError,
            InvalidParentAppointmentStatusError) as e:
        raise ValidationError(str(e))
    else:
        return _appointment.appointment


def create_call_reminder(title, start_date, reminder_time, repeat,
                         end_date=None):
    reminder_model_cls = django_apps.get_model('flourish_calendar.reminder')
    reminder_model_cls.objects.update_or_create(
        title=title,
        repeat=repeat,
        defaults={'start_date': start_date,
                  'end_date': end_date,
                  'remainder_time': reminder_time})


def check_dt_before_child_dob(subject_identifier, reference_date):
    child_consent_cls = django_apps.get_model(
        'flourish_caregiver.caregiverchildconsent')

    child_consent = child_consent_cls.objects.only(
        'child_dob').filter(subject_identifier=subject_identifier).order_by(
            '-consent_datetime').first()
    child_dob = getattr(child_consent, 'child_dob', None)
    if not child_dob:
        return None
    return child_dob < reference_date
