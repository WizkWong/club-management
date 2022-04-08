from django.contrib.auth.models import User

def object_all():
    return User.objects.all()
