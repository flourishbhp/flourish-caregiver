from django.apps import apps as django_apps
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_base.utils import age, get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from ..helper_classes import Cohort
from .antenatal_enrollment import AntenatalEnrollment
from .maternal_dataset import MaternalDataset
from .locator_logs import LocatorLog, LocatorLogEntry
from .caregiver_child_consent import CaregiverChildConsent


class PreFlourishError(Exception):
    pass


@receiver(post_save, weak=False, sender=LocatorLogEntry,
          dispatch_uid='locator_log_entry_on_post_save')
def locator_log_entry_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Create locator log entry
    """
    if not raw:
        if created:
            if not User.objects.filter(username=instance.user_created, groups__name='locator users').exists():
                try:
                    User.objects.get(username=instance.user_created)
                except User.DoesNotExist:
                    raise ValueError(f'The user {instance.user_created}, does not exist.')
                else:
                    Group.objects.get(name='locator users')

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


@receiver(post_save, weak=False, sender=AntenatalEnrollment,
          dispatch_uid='antenatal_enrollment_on_post_save')
def antenatal_enrollment_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on cohort a schedule.
    """
    if not raw and instance.is_eligible:
        put_on_schedule('cohort_a', instance=instance)


@receiver(post_save, weak=False, sender=CaregiverChildConsent,
          dispatch_uid='caregiver_child_consent_on_post_save')
def caregiver_child_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Put subject on cohort a schedule after consenting on behalf of child.
    """
    child_age = age(instance.dob, get_utcnow()).years
    child_dummy_consent_cls = django_apps.get_model('flourish_child.childdummysubjectconsent')
    cohort = cohort_assigned(instance.subject_identifier)
    if not raw:
        if child_age < 7 and cohort:
#         if cohort == 'cohort_c':
#             preflourish_model_cls = django_apps.get_model('pre_flourish.onschedulepreflourish')
#             try:
#                 preflourish_model_cls.objects.using('pre_flourish').get(identity=instance.identity)
#             except preflourish_model_cls.DoesNotExist:
#                 raise  PreFlourishError('Participant is missing PreFlourish schedule.')

            put_on_schedule(cohort, instance=instance)
            instance.cohort = cohort
            instance.save_base(raw=True)

            try:
                child_dummy_consent_cls.objects.get(subject_identifier=instance.subject_identifier+'-10',
                                                    version=instance.version,)
            except child_dummy_consent_cls.DoesNotExist:
                child_dummy_consent_cls.objects.create(
                        subject_identifier=instance.subject_identifier+'-10',
                        consent_datetime=instance.consent_datetime,
                        version=instance.version,
                        dob=instance.dob,
                        cohort=cohort)
        elif child_age >= 7 and cohort:
            try:
                child_dummy_consent_obj = child_dummy_consent_cls.objects.get(
                            subject_identifier=instance.subject_identifier+'-10',
                            version=instance.version,
                            dob=instance.dob)
            except child_dummy_consent_cls.DoesNotExist:
                pass
            else:
                put_on_schedule(cohort, instance=instance)
                instance.cohort = cohort
                instance.save_base(raw=True)
    
                child_dummy_consent_obj.cohort = cohort
                child_dummy_consent_obj.save()


def cohort_assigned(subject_identifier):
    """Calculates participant's cohort based on the maternal and child dataset
    """
    try:
        maternal_dataset_obj = MaternalDataset.objects.get(subject_identifier=subject_identifier)
    except MaternalDataset.DoesNotExist:
        return None
    else:
        infant_dataset_cls = django_apps.get_model('flourish_child.childdataset')
        try:
            infant_dataset_obj = infant_dataset_cls.objects.get(study_child_identifier=maternal_dataset_obj.study_child_identifier)
        except infant_dataset_cls.DoesNotExist:
            return None
        else:
            cohort = Cohort(child_dob=maternal_dataset_obj.delivdt,
                       enrollment_date=infant_dataset_obj.infant_enrolldate,
                       infant_hiv_exposed=infant_dataset_obj.infant_hiv_exposed,
                       protocol=maternal_dataset_obj.protocol).cohort_variable
            return cohort

def put_on_schedule(cohort, instance=None, subject_identifier=None):
    if instance:
        subject_identifier = subject_identifier or instance.subject_identifier

        cohort_label_lower = ''.join(cohort.split('_'))
        onschedule_model = 'flourish_caregiver.onschedule'+cohort_label_lower

        _, schedule = site_visit_schedules.get_by_onschedule_model(
            onschedule_model)

        onschedule_model_cls = django_apps.get_model(onschedule_model)

        schedule_name = cohort + '_schedule_1'

        try:
            onschedule_model_cls.objects.get(
                subject_identifier=instance.subject_identifier,
                schedule_name=schedule_name)
        except onschedule_model_cls.DoesNotExist:
            schedule.put_on_schedule(
                subject_identifier=instance.subject_identifier,
                onschedule_datetime=instance.created,
                schedule_name=schedule_name)
        else:
            schedule.refresh_schedule(
                subject_identifier=instance.subject_identifier)
