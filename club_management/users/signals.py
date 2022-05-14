from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import profile, User_request
from admins.models import Request_feedback


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()


@receiver(post_save, sender=User_request)
def create_request_feedback(sender, instance, created, **kwargs):
    if created:
        Request_feedback.objects.create(request_id=instance.id, user=instance.user)
