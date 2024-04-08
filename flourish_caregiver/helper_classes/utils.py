import datetime

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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


def get_child_subject_identifier_by_visit(visit):
    """Returns the child subject identifier by visit."""
    onschedule_model_cls = django_apps.get_model(
        visit.schedule.onschedule_model)

    try:
        onschedule_obj = onschedule_model_cls.objects.get(
            subject_identifier=visit.subject_identifier,
            schedule_name=visit.schedule_name)
    except onschedule_model_cls.DoesNotExist:
        return None
    else:
        return onschedule_obj.child_subject_identifier


def get_schedule_names(instance):
    onschedules = []
    child_subject_identifier = get_child_subject_identifier_by_visit(instance)
    subject_schedule_history_model = 'edc_visit_schedule.subjectschedulehistory'
    subject_schedule_history_cls = django_apps.get_model(
        subject_schedule_history_model)

    qs = subject_schedule_history_cls.objects.filter(
        subject_identifier=instance.subject_identifier).exclude(
        Q(schedule_name__icontains='tb') | Q(
            schedule_name__icontains='facet')).values_list(
        'onschedule_model', flat=True)
    for model_name in qs:
        onschedule_model_cls = django_apps.get_model(model_name)
        try:
            onschedule_obj = onschedule_model_cls.objects.get(
                subject_identifier=instance.subject_identifier,
                child_subject_identifier=child_subject_identifier)
        except onschedule_model_cls.DoesNotExist:
            continue
        else:
            onschedules.append(onschedule_obj.schedule_name)
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
