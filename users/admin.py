from django.contrib import admin
from .models import profile, User_request, Task_assigned

admin.site.register(profile)
admin.site.register(User_request)
admin.site.register(Task_assigned)
