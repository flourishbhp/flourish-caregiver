from django import forms
from django.apps import apps as django_apps
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_action_item import site_action_items
from edc_base.utils import age, get_utcnow
from edc_constants.constants import OPEN, NEW
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from flourish_prn.action_items import CAREGIVEROFF_STUDY_ACTION
from flourish_prn.action_items import CAREGIVER_DEATH_REPORT_ACTION
from flourish_prn.models.caregiver_off_study import CaregiverOffStudy
from .antenatal_enrollment import AntenatalEnrollment
from .caregiver_child_consent import CaregiverChildConsent
from .caregiver_locator import CaregiverLocator
from .caregiver_previously_enrolled import CaregiverPreviouslyEnrolled
from .locator_logs import LocatorLog, LocatorLogEntry
from .maternal_dataset import MaternalDataset
from .maternal_delivery import MaternalDelivery
from .maternal_visit import MaternalVisit
from .subject_consent import SubjectConsent
from .tb_informed_consent import TbInformedConsent
from .ultrasound import UltraSound
from ..constants import MIN_GA_LMP_ENROL_WEEKS, MAX_GA_LMP_ENROL_WEEKS
from ..helper_classes.cohort import Cohort
from ..models import CaregiverOffSchedule, ScreeningPregWomen
from ..models import ScreeningPriorBhpParticipants


class PreFlourishError(Exception):
    pass


class ChildDatasetError(Exception):
    pass


class SubjectConsentError(Exception):
    pass


@receiver(post_save, weak=False, sender=SubjectConsent,
          dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Create locator log entry
    """
    worklist_cls = django_apps.get_model('flourish_follow.worklist')
    if not raw:
        if created:
            try:
                maternal_dataset = MaternalDataset.objects.get(
                    screening_identifier=instance.screening_identifier)
            except MaternalDataset.DoesNotExist:
                pass
            else:
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

            """
            - Update subject identifier on the screening obj when created
            """
            screening_obj = None
            try:
                screening_obj = ScreeningPregWomen.objects.get(
                    screening_identifier=instance.screening_identifier)
            except ScreeningPregWomen.DoesNotExist:
                try:
                    screening_obj = ScreeningPriorBhpParticipants.objects.get(
                        screening_identifier=instance.screening_identifier)
                except ScreeningPriorBhpParticipants.DoesNotExist:
                    pass
            if screening_obj and instance.subject_identifier:
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
                            study_maternal_identifier=maternal_dataset.study_maternal_identifier)
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
    child_consent = CaregiverChildConsent.objects.filter(
        preg_enroll=True, subject_identifier__startswith=instance.subject_identifier)

    child_subject_identifier = None

    if child_consent:
        child_subject_identifier = child_consent[0].subject_identifier

        child_dummy_consent_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')

        children_count = 1 + child_dummy_consent_cls.objects.filter(
            subject_identifier__startswith=instance.subject_identifier
        ).exclude(subject_identifier__in=[child_consent[0].subject_identifier,
                                          instance.subject_identifier + '-35',
                                          instance.subject_identifier + '-46',
                                          instance.subject_identifier + '-56']).count()

        if not raw and instance.is_eligible:
            put_on_schedule('cohort_a_antenatal', instance=instance,
                            subject_identifier=instance.subject_identifier,
                            child_subject_identifier=child_subject_identifier,
                            caregiver_visit_count=children_count)


@receiver(post_save, weak=False, sender=MaternalDelivery,
          dispatch_uid='maternal_delivery_on_post_save')
def maternal_delivery_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put new born child on schedule
    """
    tb_informed_consent_cls = django_apps.get_model(
        'flourish_caregiver.tbinformedconsent')

    child_consents=get_child_consents(instance.subject_identifier)

    if instance.live_infants_to_register == 1:
        if not raw and created:
            put_on_schedule(
                'cohort_a_birth', instance=instance,
                subject_identifier=instance.subject_identifier,
                child_subject_identifier=child_consents[0].subject_identifier,
                base_appt_datetime=instance.delivery_datetime.replace(microsecond=0))
            create_registered_infant(instance)
        try:
            tb_informed_consent_cls.objects.get(
                subject_identifier=instance.subject_identifier)
        except tb_informed_consent_cls.DoesNotExist:
            pass
        else:
            put_on_schedule(
                'cohort_a_tb_2_months', instance=instance,
                subject_identifier=instance.subject_identifier,
                child_subject_identifier=child_consents[0].subject_identifier,
                base_appt_datetime=instance.delivery_datetime.replace(
                    microsecond=0))


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
    if not raw and instance.is_eligible:

        child_dummy_consent_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')

        child_age = None
        children_count = instance.caregiver_visit_count

        if not children_count:
            children_count = 1 + child_dummy_consent_cls.objects.filter(
                subject_identifier__startswith=instance.subject_consent.subject_identifier
            ).exclude(dob=instance.child_dob, ).count()

        if instance.child_dob:
            child_age = age(instance.child_dob, get_utcnow())

        if not instance.cohort:

            cohort = cohort_assigned(instance.study_child_identifier,
                                     instance.child_dob,
                                     instance.subject_consent.created.date())

            if not cohort and screening_preg_exists(instance):
                cohort = 'cohort_a'

            if child_age is not None and child_age.years < 7:
                try:
                    child_dummy_consent_cls.objects.get(
                        identity=instance.identity,
                        subject_identifier=instance.subject_identifier,
                        version=instance.subject_consent.version, )
                except child_dummy_consent_cls.DoesNotExist:

                    child_dummy_consent_cls.objects.create(
                        subject_identifier=instance.subject_identifier,
                        consent_datetime=instance.consent_datetime,
                        identity=instance.identity,
                        dob=instance.child_dob,
                        version=instance.subject_consent.version,
                        cohort=cohort)

            instance.cohort = cohort
            instance.save_base(raw=True)

            if created:
                instance.caregiver_visit_count = children_count
        else:

            try:
                prev_enrolled_obj = CaregiverPreviouslyEnrolled.objects.get(
                    subject_identifier=instance.subject_consent.subject_identifier)
            except CaregiverPreviouslyEnrolled.DoesNotExist:
                pass
            else:
                if child_age:
                    if instance.subject_identifier[-3:] not in ['-35', '-46',
                                                                '-56']:
                        put_cohort_onschedule(
                            instance.cohort,
                            instance,
                            base_appt_datetime=prev_enrolled_obj.report_datetime.replace(
                                microsecond=0))

                    try:
                        child_dummy_consent = child_dummy_consent_cls.objects.get(
                            subject_identifier=instance.subject_identifier,
                            version=instance.subject_consent.version,
                            identity=instance.identity)
                    except child_dummy_consent_cls.DoesNotExist:
                        pass
                    else:
                        if not child_dummy_consent.cohort:
                            child_dummy_consent.cohort = instance.cohort
                        child_dummy_consent.save()


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

    if not raw and created and instance.visit_code in ['2000M', '2000D']:

        if 'sec' in instance.schedule_name:

            cohort_list = instance.schedule_name.split('_')

            caregiver_visit_count = cohort_list[1][-1:]

            cohort = '_'.join(['cohort', cohort_list[0], 'sec_quart'])

        else:
            cohort_list = instance.schedule_name.split('_')

            caregiver_visit_count = cohort_list[1][-1:]

            cohort = '_'.join(['cohort', cohort_list[0], 'quarterly'])

        put_on_schedule(cohort, instance=instance,
                        subject_identifier=instance.subject_identifier,
                        child_subject_identifier=instance.subject_identifier,
                        base_appt_datetime=instance.created.replace(
                            microsecond=0),
                        caregiver_visit_count=caregiver_visit_count)

    # complete_child_crfs=AutoCompleteChildCrfs(instance=instance)
    # complete_child_crfs.pre_fill_crfs()


@receiver(post_save, weak=False, sender=CaregiverOffStudy,
          dispatch_uid='caregiver_off_study_on_post_save')
def maternal_caregiver_take_off_study(sender, instance, raw, created, **kwargs):
    for visit_schedule in site_visit_schedules.visit_schedules.values():
        for schedule in visit_schedule.schedules.values():
            onschedule_model_obj = get_onschedule_model_obj(
                schedule, instance.subject_identifier)
            if onschedule_model_obj:
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=onschedule_model_obj._meta.label_lower,
                    name=onschedule_model_obj.schedule_name)
                schedule.take_off_schedule(
                    subject_identifier=instance.subject_identifier)


@receiver(post_save, weak=False, sender=CaregiverOffSchedule,
          dispatch_uid='caregiver_off_schedule_on_post_save')
def maternal_caregiver_take_off_schedule(sender, instance, raw, created, **kwargs):
    for visit_schedule in site_visit_schedules.visit_schedules.values():
        for schedule in visit_schedule.schedules.values():
            onschedule_model_obj = get_onschedule_model_obj(
                schedule, instance.subject_identifier)
            if onschedule_model_obj and onschedule_model_obj.schedule_name == instance.schedule_name:
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=onschedule_model_obj._meta.label_lower,
                    name=instance.schedule_name)
                schedule.take_off_schedule(
                    subject_identifier=instance.subject_identifier)


@receiver(post_save, weak=False, sender=UltraSound,
          dispatch_uid='ultrasound_on_post_save')
def ultrasound_on_post_save(sender, instance, raw, created, **kwargs):
    caregiver_offstudy_cls = django_apps.get_model(
        'flourish_prn.caregiveroffstudy')

    registration_datetime = get_registration_date(instance.subject_identifier)
    if registration_datetime:
        weeks_diff = (instance.report_datetime - registration_datetime).days / 7

        ga_confirmed_after = instance.ga_confirmed - weeks_diff

        if (ga_confirmed_after < MIN_GA_LMP_ENROL_WEEKS
                or ga_confirmed_after > MAX_GA_LMP_ENROL_WEEKS):

            trigger_action_item(caregiver_offstudy_cls,
                                CAREGIVEROFF_STUDY_ACTION,
                                instance.subject_identifier)
        else:
            trigger_action_item(caregiver_offstudy_cls,
                                CAREGIVEROFF_STUDY_ACTION,
                                instance.subject_identifier,
                                opt_trigger=False)


@receiver(post_save, weak=False, sender=ScreeningPregWomen,
          dispatch_uid='screening_preg_women_on_post_save')
def screening_preg_women(sender, instance, raw, created, **kwargs):
    if not raw:
        subject_consents = SubjectConsent.objects.filter(
            screening_identifier=instance.screening_identifier)

        if not subject_consents:
            create_consent_version(instance, version=2)


@receiver(post_save, weak=False, sender=ScreeningPriorBhpParticipants,
          dispatch_uid='screening_prior_bhp_participants_on_post_save')
def screening_prior_bhp_participants(sender, instance, raw, created, **kwargs):
    if not raw:

        subject_consents = SubjectConsent.objects.filter(
            screening_identifier=instance.screening_identifier)

        if not subject_consents:
            create_consent_version(instance, version=2)


@receiver(post_save, weak=False, sender=TbInformedConsent,
          dispatch_uid='tb_informed_consent_on_post_save')
def tb_informed_consent_post_save(sender, instance, raw, created, **kwargs):
    """
    Put subject on tb enrolment schedule after tv informed consent
    """
    maternal_delivery_cls = django_apps.get_model('flourish_caregiver.maternaldelivery')
    if not raw:
        try:
            maternal_delivery_obj = maternal_delivery_cls.objects.get(
                subject_identifier=instance.subject_identifier)
        except maternal_delivery_cls.DoesNotExist:
            pass
        else:
            maternal_delivery_obj.save_base(raw=True)


def screening_preg_exists(caregiver_child_consent_obj):
    preg_women_screening_cls = django_apps.get_model(
        'flourish_caregiver.screeningpregwomen')

    try:
        preg_women_screening_cls.objects.get(
            screening_identifier=caregiver_child_consent_obj.subject_consent.screening_identifier)
    except preg_women_screening_cls.DoesNotExist:
        return False
    else:
        return True


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
        pass
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
        assent_obj = child_assent_cls.objects.get(
            subject_identifier=subject_identifier)
    except child_assent_cls.DoesNotExist:
        return None
    else:
        return assent_obj.created.replace(microsecond=0)


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
        schedule, onschedule_model_cls, schedule_name = get_onschedule_model(
            cohort=cohort,
            caregiver_visit_count=caregiver_visit_count,
            subject_identifier=subject_identifier,
            instance=instance)

        assent_onschedule_datetime = get_assent_onschedule_datetime(
            subject_identifier)
        schedule.put_on_schedule(
            subject_identifier=subject_identifier,
            onschedule_datetime=(base_appt_datetime
                                 or assent_onschedule_datetime
                                 or instance.created.replace(microsecond=0)),
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
                onschedule_obj.child_subject_identifier = (child_subject_identifier
                                                           or instance.subject_identifier)
                onschedule_obj.save()


def get_onschedule_model(cohort, caregiver_visit_count=None, subject_identifier=None,
        instance=None):
    cohort_label_lower = ''.join(cohort.split('_'))

    if 'enrol' in cohort:
        cohort_label_lower = cohort_label_lower.replace('enrol', 'enrollment')

    onschedule_model = 'flourish_caregiver.onschedule' + cohort_label_lower

    children_count = str(get_schedule_sequence(
        subject_identifier,
        instance,
        django_apps.get_model(onschedule_model),
        caregiver_visit_count=caregiver_visit_count))
    cohort = cohort + children_count

    if 'pool' not in cohort:
        cohort = cohort.replace('cohort_', '')

    schedule_name = cohort + '_schedule1'

    if 'tb_2_months' in cohort:
        onschedule_model = 'flourish_caregiver.onschedule' + cohort_label_lower
        schedule_name = 'tb_2_months_schedule'

    _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
        onschedule_model=onschedule_model, name=schedule_name)

    onschedule_model_cls = django_apps.get_model(onschedule_model)

    return schedule, onschedule_model_cls, schedule_name


def get_onschedule_model_obj(schedule, subject_identifier):
    try:
        return schedule.onschedule_model_cls.objects.get(
            subject_identifier=subject_identifier)
    except ObjectDoesNotExist:
        return None


def get_registration_date(subject_identifier):
    child_consents=get_child_consents(subject_identifier)
    if (child_consents and child_consents.values_list(
            'subject_identifier', flat=True).distinct().count() == 1):
        child_consent = child_consents[0]
        return child_consent.consent_datetime
    else:
        raise forms.ValidationError(
            'Missing matching Child Subject Consent form, cannot proceed.')


def create_registered_infant(instance):
    #  Create infant registered subject
    if isinstance(instance, MaternalDelivery):
        if instance.live_infants_to_register == 1:
            maternal_consent = SubjectConsent.objects.filter(
                subject_identifier=instance.subject_identifier
            ).order_by('version').last()
            try:
                UltraSound.objects.filter(
                    maternal_visit__subject_identifier=instance.subject_identifier
                ).order_by('report_datetime').last()
            except UltraSound.DoesNotExist:
                raise ValidationError(
                    'Maternal Ultrasound must exist for {instance.subject_identifier}')
            else:
                with transaction.atomic():
                    caregiver_child_consent_cls = django_apps.get_model(
                        'flourish_caregiver.caregiverchildconsent')

                    # Create caregiver child consent
                    try:
                        caregiver_child_consent_obj = caregiver_child_consent_cls.objects.get(
                            subject_identifier__startswith=instance.subject_identifier,
                            version=maternal_consent.version)
                    except caregiver_child_consent_cls.DoesNotExist:
                        caregiver_child_consent_cls.objects.create(
                            subject_consent=maternal_consent,
                            version=maternal_consent.version,
                            child_dob=instance.delivery_datetime.date(),
                            consent_datetime=get_utcnow(),
                            is_eligible=True)
                    else:
                        child_dummy_consent_cls = django_apps.get_model(
                            'flourish_child.childdummysubjectconsent')
                        try:
                            dummy_consent_obj = child_dummy_consent_cls.objects.get(
                                subject_identifier=caregiver_child_consent_obj.subject_identifier,
                                version=caregiver_child_consent_obj.version)
                        except child_dummy_consent_cls.DoesNotExist:
                            child_dummy_consent_cls.objects.create(
                                subject_identifier=caregiver_child_consent_obj.subject_identifier,
                                consent_datetime=caregiver_child_consent_obj.consent_datetime,
                                dob=caregiver_child_consent_obj.dob,
                                cohort=caregiver_child_consent_obj.cohort,
                                version=caregiver_child_consent_obj.version)


def trigger_action_item(model_cls, action_name, subject_identifier,
        repeat=False, opt_trigger=True
):
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
            user_created=instance.user_modified or instance.user_created,
            created=get_utcnow())
        consent_version.save()


def get_child_consents(subject_identifier):
    child_consent_cls = django_apps.get_model('flourish_caregiver.caregiverchildconsent')
    return child_consent_cls.objects.filter(
        subject_identifier__startswith=subject_identifier).order_by('-consent_datetime')
