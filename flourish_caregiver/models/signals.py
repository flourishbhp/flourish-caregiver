from django.db.models.signals import post_save
from django.dispatch import receiver

from django.apps import apps as django_apps

from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .enrollment import Enrollment

from .maternal_dataset import MaternalDataset
from .locator_logs import LocatorLog


@receiver(post_save, weak=False, sender=MaternalDataset,
          dispatch_uid='maternal_dataset_on_post_save')
def maternal_dataset_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Create locator log entry
    """
    if not raw:
        if created:

            try:
                LocatorLog.objects.get(
                    maternal_dataset=instance)
            except LocatorLog.DoesNotExist:
                LocatorLog.objects.create(
                    maternal_dataset=instance)
   

@receiver(post_save, weak=False, sender=Enrollment,
          dispatch_uid='enrollment_on_post_save')
def enrollment_on_post_save(sender, instance, raw, created, **kwargs):
    """Update subject on schedule.
    """
    if not raw and instance.child_age:
        schedule_map = {'lt_3': 'a',
                        'gt_3_lt_10': 'b',
                        'gt_10': 'c'}
        put_on_schedule(schedule_map.get(instance.child_age),
                        instance=instance)

def put_on_schedule(cohort, instance=None):
    if instance:
        
        onschedule_model = 'flourish_caregiver.onschedulecohort'+cohort
        _, schedule = site_visit_schedules.get_by_onschedule_model(
            onschedule_model)
        
        onschedule_model_cls = django_apps.get_model(onschedule_model)
        
        schedule_name = 'cohort_' + cohort + '_schedule_1'
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
