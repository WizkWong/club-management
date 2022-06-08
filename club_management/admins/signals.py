from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from users.models import Task_assigned
from .models import Page
from club_management.settings import MEDIA_URL
import os


@receiver(pre_delete, sender=Task_assigned)
def delete_task_file(sender, instance, **kwargs):
    if os.path.exists(f'{MEDIA_URL.replace("/", "")}/{instance.upload_file}'):
        os.remove(f'{MEDIA_URL.replace("/", "")}/{instance.upload_file}')


@receiver(pre_save, sender=Page)
def replace_image(sender, instance, **kwargs):
    page = Page.objects.first()
    if page is None:
        return

    if not(str(instance.top_background).startswith('page')):
        page = Page.objects.get(id=instance.id)
        if page.top_background:
            if os.path.exists(f'{MEDIA_URL.replace("/", "")}/{page.top_background}'):
                os.remove(f'{MEDIA_URL.replace("/", "")}/{page.top_background}')

    if not(str(instance.image).startswith('page')):
        page = Page.objects.get(id=instance.id)
        if page.image:
            if os.path.exists(f'{MEDIA_URL.replace("/", "")}/{page.image}'):
                os.remove(f'{MEDIA_URL.replace("/", "")}/{page.image}')
