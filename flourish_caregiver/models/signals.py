from django.apps import apps as django_apps
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_base.utils import age, get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from ..helper_classes.cohort import Cohort
from .antenatal_enrollment import AntenatalEnrollment
from .maternal_dataset import MaternalDataset
from .locator_logs import LocatorLog, LocatorLogEntry
from .caregiver_child_consent import CaregiverChildConsent
from .maternal_delivery import MaternalDelivery
from flourish_caregiver.models.subject_consent import SubjectConsent


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
            if not User.objects.filter(username=instance.user_created,
                                       groups__name='locator users').exists():
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
    """
    - Put subject on cohort a schedule.
    """
    child_dummy_consent_cls = django_apps.get_model(
                'flourish_child.childdummysubjectconsent')
    children_count = 1 + child_dummy_consent_cls.objects.filter(
                subject_identifier__icontains=instance.subject_identifier).count()

    if not raw and instance.is_eligible:
        put_on_schedule(('cohort_a_enrol' + str(children_count)), instance=instance)
        put_on_schedule(('cohort_a_quarterly' + str(children_count)), instance=instance)


@receiver(post_save, weak=False, sender=MaternalDelivery,
          dispatch_uid='maternal_delivery_on_post_save')
def maternal_delivery_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put new born child on schedule
    """
    if not raw:
        if created and instance.live_infants_to_register == 1:

            try:
                consent_obj = SubjectConsent.objects.get(
                    subject_identifier=instance.subject_identifier)
            except SubjectConsent.DoesNotExist:
                raise
            else:

                child_dummy_consent_cls = django_apps.get_model(
                    'flourish_child.childdummysubjectconsent')

                children_count = 1 + child_dummy_consent_cls.objects.filter(
                    subject_identifier__icontains=instance.subject_identifier
                    ).count()
                child_identifier_postfix = '-' + str(children_count * 10)

                put_on_schedule(('cohort_a_birth' + str(children_count)), instance=instance)

                child_dummy_consent_cls.objects.create(
                    subject_identifier=(
                        instance.subject_identifier + child_identifier_postfix),
                    consent_datetime=instance.delivery_datetime,
                    version=consent_obj.version,
                    cohort='cohort_a')


@receiver(post_save, weak=False, sender=CaregiverChildConsent,
          dispatch_uid='caregiver_child_consent_on_post_save')
def caregiver_child_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put subject on cohort a schedule after consenting on behalf of child.
    """

    if not raw and instance.is_eligible:

        cohort = cohort_assigned(instance.subject_consent.screening_identifier,
                                 instance.child_dob)

        if cohort:

            child_dummy_consent_cls = django_apps.get_model(
                'flourish_child.childdummysubjectconsent')

            children_count = 1 + child_dummy_consent_cls.objects.filter(
                subject_identifier__icontains=instance.subject_consent.subject_identifier
                ).exclude(identity=instance.identity).count()
            child_age = age(instance.child_dob, get_utcnow()).years

            if child_age and child_age < 7:

                put_on_schedule((cohort + '_enrol' + str(children_count)),
                                instance=instance.subject_consent)
                put_on_schedule((cohort + '_quarterly' + str(children_count)),
                                instance=instance.subject_consent)

                try:
                    child_dummy_consent_obj = child_dummy_consent_cls.objects.get(
                        identity=instance.identity,
                        version=instance.subject_consent.version,)
                except child_dummy_consent_cls.DoesNotExist:

                    child_dummy_consent_cls.objects.create(
                            subject_identifier=instance.subject_identifier,
                            consent_datetime=instance.consent_datetime,
                            identity=instance.identity,
                            version=instance.subject_consent.version,
                            cohort=cohort)
                else:
                    if not child_dummy_consent_obj.cohort:
                        child_dummy_consent_obj.cohort = cohort
                        child_dummy_consent_obj.save()

            else:
                try:
                    child_dummy_consent_cls.objects.get(
                                subject_identifier=instance.subject_identifier,
                                version=instance.subject_consent.version,
                                identity=instance.identity)
                except child_dummy_consent_cls.DoesNotExist:
                    pass
                else:
                    put_on_schedule((cohort + '_enrol' + str(children_count)),
                                    instance=instance.subject_consent)
                    put_on_schedule((cohort + '_quarterly' + str(children_count)),
                                    instance=instance.subject_consent)

            instance.cohort = cohort
            instance.save_base(raw=True)


def cohort_assigned(screening_identifier, child_dob):
    """Calculates participant's cohort based on the maternal and child dataset
    """
    try:
        maternal_dataset_obj = MaternalDataset.objects.get(
            screening_identifier=screening_identifier)
    except MaternalDataset.DoesNotExist:
        return None
    else:
        infant_dataset_cls = django_apps.get_model('flourish_child.childdataset')
        try:
            infant_dataset_obj = infant_dataset_cls.objects.get(
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)
        except infant_dataset_cls.DoesNotExist:
            raise
        else:
            cohort = Cohort(
                child_dob=child_dob,
                enrollment_date=get_utcnow().date(),
                infant_hiv_exposed=infant_dataset_obj.infant_hiv_exposed,
                protocol=maternal_dataset_obj.protocol,
                mum_hiv_status=maternal_dataset_obj.mom_hivstatus,
                dtg=maternal_dataset_obj.preg_dtg,
                efv=maternal_dataset_obj.preg_efv,
                pi=maternal_dataset_obj.preg_pi).cohort_variable
            return cohort


def put_on_schedule(cohort, instance=None, subject_identifier=None):
    if instance:
        subject_identifier = subject_identifier or instance.subject_identifier

        cohort_label_lower = ''.join(cohort[:-1].split('_'))

        if 'enrol' in cohort:
            cohort_label_lower = cohort_label_lower.replace('enrol', 'enrollment')

        onschedule_model = 'flourish_caregiver.onschedule' + cohort_label_lower

        _, schedule = site_visit_schedules.get_by_onschedule_model(
            onschedule_model)

        onschedule_model_cls = django_apps.get_model(onschedule_model)

        if 'pool' not in cohort:
            cohort = cohort.replace('cohort_', '')
        schedule_name = cohort + '_schedule1'
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
                subject_identifier=instance.subject_identifier,
                schedule_name=schedule_name)
