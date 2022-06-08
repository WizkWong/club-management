from django.db.models.signals import post_save, pre_delete, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import profile, User_request, Task_assigned
from admins.models import Request_feedback
from club_management.settings import MEDIA_URL
import os


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)


@receiver(pre_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    if instance.profile.image == 'default.jpg':
        return
    else:
        if os.path.exists(f'{MEDIA_URL.replace("/", "")}/{instance.profile.image}'):
            os.remove(f'{MEDIA_URL.replace("/", "")}/{instance.profile.image}')


@receiver(pre_save, sender=User)
def replace_profile(sender, instance, **kwargs):
    if User.objects.filter(id=instance.id).exists():

        if str(instance.profile.image).startswith('profile_pics'):
            return

        else:
            old = User.objects.get(id=instance.id)
            if old.profile.image == 'default.jpg':
                return
            else:
                if os.path.exists(f'{MEDIA_URL.replace("/", "")}/{old.profile.image}'):
                    os.remove(f'{MEDIA_URL.replace("/", "")}/{old.profile.image}')


@receiver(post_save, sender=User_request)
def create_request_feedback(sender, instance, created, **kwargs):
    if created:
        Request_feedback.objects.create(request=instance, user=instance.user)


@receiver(pre_save, sender=Task_assigned)
def replace_save_file(sender, instance, **kwargs):
    if Task_assigned.objects.filter(task=instance.task, user=instance.user).exists():

        if str(instance.upload_file).startswith('files'):
            return

        else:
            old_file = Task_assigned.objects.get(task=instance.task, user=instance.user)
            if old_file is not None:
                if old_file.upload_file:
                    if os.path.exists(f'{MEDIA_URL.replace("/", "")}/{old_file.upload_file}'):
                        os.remove(f'{MEDIA_URL.replace("/", "")}/{old_file.upload_file}')
                else:
                    return
