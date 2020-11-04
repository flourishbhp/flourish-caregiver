from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .subject_consent import SubjectConsent
from .onschedule import OnScheduleCohortB

@receiver(post_save, weak=False, sender=SubjectConsent,
          dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Update subject screening consented flag.
    """
    if not raw:
        put_on_schedule(instance=instance)

def put_on_schedule(instance=None):
    if instance:

        _, schedule = site_visit_schedules.get_by_onschedule_model(
            'flourish_caregiver.onschedule')

        try:
            OnScheduleCohortB.objects.get(
                subject_identifier=instance.subject_identifier,
                schedule_name='cohort_b_schedule_1')
        except OnScheduleCohortB.DoesNotExist:
            schedule.put_on_schedule(
                subject_identifier=instance.subject_identifier,
                onschedule_datetime=instance.consent_datetime,
                schedule_name='cohort_b_schedule_1')
        else:
            schedule.refresh_schedule(
                subject_identifier=instance.subject_identifier)
