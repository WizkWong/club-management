from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import profile, User_request
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


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()


@receiver(post_save, sender=User_request)
def create_request_feedback(sender, instance, created, **kwargs):
    if created:
        Request_feedback.objects.create(request=instance, user=instance.user)
