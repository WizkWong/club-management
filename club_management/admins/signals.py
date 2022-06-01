from django.db.models.signals import pre_delete
from django.dispatch import receiver
from users.models import Task_assigned
import os


@receiver(pre_delete, sender=Task_assigned)
def delete_profile(sender, instance, **kwargs):
    if os.path.exists(f'media/{instance.upload_file}'):
        os.remove(f'media/{instance.upload_file}')
