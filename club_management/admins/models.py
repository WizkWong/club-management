from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import User_request


class Event(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    datetime_created = models.DateTimeField(default=timezone.now)
    detail = models.TextField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Attendance_of_user(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = (('event', 'user'),)


class Task(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    datetime_created = models.DateTimeField(default=timezone.now)
    detail = models.TextField(null=True)
    deadline = models.DateTimeField()


class Request_feedback(models.Model):
    request = models.OneToOneField(User_request, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    accept = models.BooleanField(null=True)
    feedback = models.TextField(null=True)


class Report(models.Model):
    ATTENDANCE = 'ATD'
    EVENT = 'EVT'
    TYPE = {
        (ATTENDANCE, 'Attendance'),
        (EVENT, 'Event')
    }
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=3, choices=TYPE)
    content = models.TextField(null=True)
    datetime_created = models.DateTimeField(default=timezone.now)

