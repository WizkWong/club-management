from django.contrib import admin
from .models import Event, Attendance_of_user, Task, Request_feedback, Report

admin.site.register(Event)
admin.site.register(Attendance_of_user)
admin.site.register(Task)
admin.site.register(Request_feedback)
admin.site.register(Report)
