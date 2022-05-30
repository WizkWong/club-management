from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Event(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    datetime_created = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100)
    detail = models.TextField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Attendance_of_user(models.Model):
    LATE = 2
    PRESENT = 1
    ABSENT = 0

    ATTENDANCE = {
        (LATE, 'Late'),
        (PRESENT, 'Present'),
        (ABSENT, 'Absent')
    }
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance = models.IntegerField(choices=ATTENDANCE, default=ABSENT)

    class Meta:
        unique_together = (('event', 'user'),)


class Task(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    datetime_created = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100)
    detail = models.TextField(null=True)
    deadline = models.DateTimeField()


class Request_feedback(models.Model):
    PENDING = 2
    ACCEPT = 1
    REJECT = 0

    APPROVAL = {
        (PENDING, 'Pending'),
        (ACCEPT, 'Accept'),
        (REJECT, 'Reject')
    }
    """
    do not use "from users.models import User_request" for the request one to one field to
    avoid the circular import error
    """
    request = models.OneToOneField('users.User_request', on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    approval = models.IntegerField(choices=APPROVAL, default=PENDING)
    feedback = models.TextField(null=True, default=None)


class Report(models.Model):
    ATTENDANCE = 'ATD'
    EVENT = 'EVT'
    TYPE = {
        (ATTENDANCE, 'Attendance'),
        (EVENT, 'Event')
    }
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=3, choices=TYPE)
    content = models.TextField(null=True)
    datetime_created = models.DateTimeField(default=timezone.now)

