from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from admins.models import Task


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'Profile: {self.user.username}'


class User_request(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    detail = models.TextField()
    datetime_created = models.DateTimeField(default=timezone.now)


class Task_assigned(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    upload_file = models.FileField(null=True, upload_to='files', default=None)
    complete = models.BooleanField(default=False)
    datetime_complete = models.DateTimeField(null=True, default=None)

    class Meta:
        unique_together = (('task', 'user'),)
