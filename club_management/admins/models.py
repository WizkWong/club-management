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


class Page(models.Model):
    title_page = models.CharField(null=True, default=None, max_length=30)
    title_text = models.TextField(null=True, default=None)
    paragraph1 = models.TextField(null=True, default=None)
    paragraph2 = models.TextField(null=True, default=None)
    paragraph3 = models.TextField(null=True, default=None)
    about_us = models.TextField(null=True, default=None)
    phone_number = models.IntegerField(null=True, default=None)
    email = models.EmailField(null=True, default=None)
    top_background = models.ImageField(null=True, default=None, upload_to='page')
    image = models.ImageField(null=True, default=None, upload_to='page')

