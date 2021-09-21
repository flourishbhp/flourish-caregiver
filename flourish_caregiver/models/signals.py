from django.apps import apps as django_apps
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_base.utils import age, get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
import flourish_follow.models
from ..helper_classes.cohort import Cohort
from .antenatal_enrollment import AntenatalEnrollment
from .caregiver_child_consent import CaregiverChildConsent
from .caregiver_locator import CaregiverLocator
from .locator_logs import LocatorLog, LocatorLogEntry
from .maternal_dataset import MaternalDataset
from .maternal_delivery import MaternalDelivery
from .caregiver_previously_enrolled import CaregiverPreviouslyEnrolled
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
                            study_maternal_identifier=maternal_dataset.study_maternal_identifier)
                    except child_dataset_cls.DoesNotExist:
                        raise
                    else:
                        offstudy_td = child_dataset.infant_offstudy_complete == 1

                if offstudy_td:
                    try:

                        flourish_follow.models.WorkList.objects.get(
                            study_maternal_identifier=instance.study_maternal_identifier)
                    except flourish_follow.models.WorkList.DoesNotExist:
                        flourish_follow.models.WorkList.objects.create(
                            study_maternal_identifier=instance.study_maternal_identifier,
                            prev_study=maternal_dataset.protocol,
                            user_created=instance.user_created)


@receiver(post_save, weak=False, sender=AntenatalEnrollment,
          dispatch_uid='antenatal_enrollment_on_post_save')
def antenatal_enrollment_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put subject on cohort a schedule.
    """
    if not raw and instance.is_eligible:
        put_on_schedule('cohort_a_antenatal', instance=instance,
                        subject_identifier=instance.subject_identifier)


@receiver(post_save, weak=False, sender=MaternalDelivery,
          dispatch_uid='maternal_delivery_on_post_save')
def maternal_delivery_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put new born child on schedule
    """
    pass
    # if not raw:
        # if created and instance.live_infants_to_register == 1:
            # put_on_schedule('cohort_a_birth', instance=instance,
                            # subject_identifier=instance.subject_identifier)
            # put_on_schedule('cohort_a_quarterly', instance=instance,
                            # subject_identifier=instance.subject_identifier)


@receiver(post_save, weak=False, sender=CaregiverPreviouslyEnrolled,
          dispatch_uid='caregiver_previously_enrolled_on_post_save')
def caregiver_previously_enrolled_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put subject with participation on schedule after consenting.
    """
    if not raw:

        child_assent_cls = django_apps.get_model('flourish_child.childassent')

        child_assents = child_assent_cls.objects.filter(
            subject_identifier__startswith=instance.subject_identifier)

        for child in child_assents:
            child.save()

        child_identifiers = child_assent_cls.objects.filter(
            subject_identifier__startswith=instance.subject_identifier).values_list(
                'subject_identifier')

        child_consents = CaregiverChildConsent.objects.filter(
            subject_identifier__startswith=instance.subject_identifier).exclude(
                subject_identifier__in=child_identifiers)

        for child in child_consents:
            child.save()


@receiver(post_save, weak=False, sender=CaregiverChildConsent,
          dispatch_uid='caregiver_child_consent_on_post_save')
def caregiver_child_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put subject on cohort a schedule after consenting on behalf of child.
    """

    try:
        prev_enrolled_obj = CaregiverPreviouslyEnrolled.objects.get(
            subject_identifier=instance.subject_consent.subject_identifier)
    except CaregiverPreviouslyEnrolled.DoesNotExist:
        pass
    else:
        if not raw and instance.is_eligible:

            cohort = cohort_assigned(instance.study_child_identifier,
                                     instance.child_dob,
                                     instance.subject_consent.created)

            if cohort:
                children_count = instance.caregiver_visit_count
                child_dummy_consent_cls = django_apps.get_model(
                    'flourish_child.childdummysubjectconsent')

                if not children_count:
                    children_count = 1 + child_dummy_consent_cls.objects.filter(
                        subject_identifier__startswith=instance.subject_consent.subject_identifier
                        ).exclude(dob=instance.child_dob,).count()

                child_age = age(instance.child_dob, get_utcnow()).years

                if child_age and child_age < 7:

                    if instance.subject_identifier[-3:] not in ['-35', '-46', '-56']:
                        put_cohort_onschedule(cohort,
                                              instance,
                                              base_appt_datetime=prev_enrolled_obj.created)

                    try:
                        child_dummy_consent_obj = child_dummy_consent_cls.objects.get(
                            identity=instance.identity,
                            subject_identifier=instance.subject_identifier,
                            version=instance.subject_consent.version,)
                    except child_dummy_consent_cls.DoesNotExist:

                        child_dummy_consent_cls.objects.create(
                                subject_identifier=instance.subject_identifier,
                                consent_datetime=instance.consent_datetime,
                                identity=instance.identity,
                                dob=instance.child_dob,
                                version=instance.subject_consent.version,
                                cohort=cohort)
                    else:
                        if not child_dummy_consent_obj.cohort:
                            child_dummy_consent_obj.cohort = cohort
                        child_dummy_consent_obj.save()

                elif instance.subject_identifier[-3:] not in ['-35', '-46', '-56']:

                    try:
                        child_dummy_consent = child_dummy_consent_cls.objects.get(
                                    subject_identifier=instance.subject_identifier,
                                    version=instance.subject_consent.version,
                                    identity=instance.identity)
                    except child_dummy_consent_cls.DoesNotExist:
                        pass
                    else:
                        if not child_dummy_consent.cohort:
                            child_dummy_consent.cohort = cohort
                            child_dummy_consent.save()
                        put_cohort_onschedule(cohort,
                                              instance,
                                              base_appt_datetime=prev_enrolled_obj.created)

                if created:
                    instance.caregiver_visit_count = children_count
                instance.cohort = cohort
                instance.save_base(raw=True)


def put_cohort_onschedule(cohort, instance, base_appt_datetime=None):

    if cohort is not None:
        if 'sec' in cohort:
            put_on_schedule(cohort, instance=instance,
                            child_subject_identifier=instance.subject_identifier,
                            base_appt_datetime=base_appt_datetime,
                            caregiver_visit_count=instance.caregiver_visit_count)
        else:
            put_on_schedule((cohort + '_enrol'),
                            instance=instance,
                            child_subject_identifier=instance.subject_identifier,
                            base_appt_datetime=base_appt_datetime,
                            caregiver_visit_count=instance.caregiver_visit_count)
            return put_on_schedule((cohort + '_quarterly'),
                                   instance=instance,
                                   child_subject_identifier=instance.subject_identifier,
                                   base_appt_datetime=base_appt_datetime,
                                   caregiver_visit_count=instance.caregiver_visit_count)
        # put_on_schedule((cohort + '_fu' + str(children_count)),
                        # instance=instance,
                        # child_subject_identifier=instance.subject_identifier,
                        # base_appt_datetime=django_apps.get_app_config(
                    # 'edc_protocol').study_open_datetime)


def cohort_assigned(study_child_identifier, child_dob, enrollment_date):
    """Calculates participant's cohort based on the maternal and child dataset
    """
    infant_dataset_cls = django_apps.get_model('flourish_child.childdataset')
    try:
        infant_dataset_obj = infant_dataset_cls.objects.get(
            study_child_identifier=study_child_identifier,
            dob=child_dob)
    except infant_dataset_cls.DoesNotExist:
        return None
    except infant_dataset_cls.MultipleObjectsReturned:
        infant_dataset_obj = infant_dataset_cls.objects.filter(
            study_child_identifier=study_child_identifier,
            dob=child_dob)[0]
    else:
        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                study_maternal_identifier=infant_dataset_obj.study_maternal_identifier)
        except MaternalDataset.DoesNotExist:
            return None
        else:
            if infant_dataset_obj:
                cohort = Cohort(
                    child_dob=child_dob,
                    enrollment_date=enrollment_date,
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


def get_schedule_sequence(subject_identifier, instance,
                          onschedule_cls, caregiver_visit_count=None):

    children_count = (caregiver_visit_count or
                      1 + onschedule_cls.objects.filter(
                          subject_identifier=subject_identifier).exclude(
                              child_subject_identifier=instance.subject_identifier).count())
    return children_count


def put_on_schedule(cohort, instance=None, subject_identifier=None,
                    child_subject_identifier=None, base_appt_datetime=None,
                    caregiver_visit_count=None):

    subject_identifier = subject_identifier or instance.subject_consent.subject_identifier
    if instance:

        cohort_label_lower = ''.join(cohort.split('_'))

        if 'enrol' in cohort:
            cohort_label_lower = cohort_label_lower.replace('enrol', 'enrollment')

        onschedule_model = 'flourish_caregiver.onschedule' + cohort_label_lower

        children_count = str(get_schedule_sequence(subject_identifier,
                                                   instance,
                                                   django_apps.get_model(onschedule_model),
                                                   caregiver_visit_count=caregiver_visit_count))
        cohort = cohort + children_count

        if 'pool' not in cohort:
            cohort = cohort.replace('cohort_', '')

        schedule_name = cohort + '_schedule1'

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name)

        onschedule_model_cls = django_apps.get_model(onschedule_model)

        assent_onschedule_datetime = get_assent_onschedule_datetime(subject_identifier)
        schedule.put_on_schedule(
                subject_identifier=subject_identifier,
                onschedule_datetime=(base_appt_datetime
                                     or assent_onschedule_datetime
                                     or instance.created),
                schedule_name=schedule_name,
                base_appt_datetime=base_appt_datetime)

        try:
            onschedule_model_cls.objects.get(
                subject_identifier=subject_identifier,
                schedule_name=schedule_name,
                child_subject_identifier=child_subject_identifier)
        except onschedule_model_cls.DoesNotExist:
            try:
                onschedule_obj = schedule.onschedule_model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    schedule_name=schedule_name,
                    child_subject_identifier='')
            except schedule.onschedule_model_cls.DoesNotExist:
                pass
            else:
                onschedule_obj.child_subject_identifier = instance.subject_identifier
                onschedule_obj.save()
