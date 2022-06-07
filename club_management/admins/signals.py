from django.db.models.signals import pre_delete
from django.dispatch import receiver
from users.models import Task_assigned
from club_management.settings import MEDIA_URL
import os


@receiver(pre_delete, sender=Task_assigned)
def delete_task_file(sender, instance, **kwargs):
    if os.path.exists(f'{MEDIA_URL.replace("/", "")}/{instance.upload_file}'):
        os.remove(f'{MEDIA_URL.replace("/", "")}/{instance.upload_file}')
