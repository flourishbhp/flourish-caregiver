from django.db.models.signals import post_save
from django.dispatch import receiver

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

