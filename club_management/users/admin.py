from django.contrib import admin
from .models import profile, User_request, Task_assigned, Chat, Pending_user

admin.site.register(profile)
admin.site.register(User_request)
admin.site.register(Task_assigned)
admin.site.register(Chat)
admin.site.register(Pending_user)
