from django.apps import apps as django_apps
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_base.utils import age, get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from ..helper_classes.cohort import Cohort
from .antenatal_enrollment import AntenatalEnrollment
from .caregiver_child_consent import CaregiverChildConsent
from .caregiver_locator import CaregiverLocator
from .locator_logs import LocatorLog, LocatorLogEntry
from .maternal_dataset import MaternalDataset
from flourish_follow.models import WorkList
# from .maternal_delivery import MaternalDelivery
# from flourish_caregiver.models.subject_consent import SubjectConsent


class PreFlourishError(Exception):
    pass


class ChildDatasetError(Exception):
    pass


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
                    raise ValueError(f'The user {instance.user_created}, does not exist.')
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
    if not raw:
        if created:
            try:
                maternal_dataset = MaternalDataset.objects.get(
                    study_maternal_identifier=instance.study_maternal_identifier)
            except MaternalDataset.DoesNotExist:
                pass
            else:
                try:
                    WorkList.objects.get(
                        study_maternal_identifier=instance.study_maternal_identifier)
                except WorkList.DoesNotExist:
                    WorkList.objects.create(
                        study_maternal_identifier=instance.study_maternal_identifier,
                        prev_study=maternal_dataset.protocol,
                        user_created=instance.user_created)


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
        put_on_schedule(('cohort_a_enrol' + str(children_count)),
                        instance=instance,
                        subject_identifier=instance.subject_identifier)
        put_on_schedule(('cohort_a_quarterly' + str(children_count)),
                        instance=instance,
                        subject_identifier=instance.subject_identifier)

# @receiver(post_save, weak=False, sender=MaternalDelivery,
          # dispatch_uid='maternal_delivery_on_post_save')
# def maternal_delivery_on_post_save(sender, instance, raw, created, **kwargs):
    # """
    # - Put new born child on schedule
    # """
    # if not raw:
        # if created and instance.live_infants_to_register == 1:
        #
            # pass


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
                ).exclude(identity=instance.identity,).count()
            child_age = age(instance.child_dob, get_utcnow()).years
            if child_age and child_age < 7:
                if instance.subject_identifier[-3:] not in ['-35', '-46', '-56']:
                    put_cohort_onschedule(cohort, children_count, instance)

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

            elif instance.subject_identifier[-3:] not in ['-35', '-46', '-56']:
                try:
                    child_dummy_consent_cls.objects.get(
                                subject_identifier=instance.subject_identifier,
                                version=instance.subject_consent.version,
                                identity=instance.identity)
                except child_dummy_consent_cls.DoesNotExist:
                    pass
                else:
                    put_cohort_onschedule(cohort, children_count, instance)

            instance.cohort = cohort
            instance.caregiver_visit_count = children_count
            instance.save_base(raw=True)


def put_cohort_onschedule(cohort, children_count, instance):

    if cohort is not None and 'sec' in cohort:
        put_on_schedule((cohort + str(children_count)),
                        instance=instance)
    else:
        put_on_schedule((cohort + '_enrol' + str(children_count)),
                        instance=instance)
        put_on_schedule((cohort + '_quarterly' + str(children_count)),
                        instance=instance,)
        put_on_schedule((cohort + '_fu' + str(children_count)),
                        instance=instance, base_appt_datetime=django_apps.get_app_config(
                    'edc_protocol').study_open_datetime)


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
        infant_dataset_obj = None
        try:
            infant_dataset_obj = infant_dataset_cls.objects.get(
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,
                dob=child_dob)
        except infant_dataset_cls.DoesNotExist:
            infant_dataset_obj = None
        except infant_dataset_cls.MultipleObjectsReturned:
            infant_dataset_obj = infant_dataset_cls.objects.filter(
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,
                dob=child_dob)[0]

        if infant_dataset_obj:
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


def get_assent_onschedule_datetime(subject_identifier):

    child_assent_cls = django_apps.get_model('flourish_child.childassent')

    try:
        assent_obj = child_assent_cls.objects.get(subject_identifier=subject_identifier)
    except child_assent_cls.DoesNotExist:
        return None
    else:
        return assent_obj.created


def put_on_schedule(cohort, instance=None, subject_identifier=None, base_appt_datetime=None):

    subject_identifier = subject_identifier or instance.subject_consent.subject_identifier
    if instance:

        cohort_label_lower = ''.join(cohort[:-1].split('_'))

        if 'enrol' in cohort:
            cohort_label_lower = cohort_label_lower.replace('enrol', 'enrollment')

        onschedule_model = 'flourish_caregiver.onschedule' + cohort_label_lower

        if 'pool' not in cohort:
            cohort = cohort.replace('cohort_', '')

        schedule_name = cohort + '_schedule1'

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name)

        onschedule_model_cls = django_apps.get_model(onschedule_model)

        assent_onschedule_datetime = get_assent_onschedule_datetime(subject_identifier)

        try:
            onschedule_model_cls.objects.get(
                subject_identifier=subject_identifier,
                onschedule_datetime=assent_onschedule_datetime or instance.created,
                schedule_name=schedule_name)
        except onschedule_model_cls.DoesNotExist:
            schedule.put_on_schedule(
                subject_identifier=subject_identifier,
                onschedule_datetime=assent_onschedule_datetime or instance.created,
                schedule_name=schedule_name,
                base_appt_datetime=base_appt_datetime)
        else:
            schedule.refresh_schedule(
                subject_identifier=subject_identifier,
                schedule_name=schedule_name)
