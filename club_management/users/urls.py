from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profile, name='user-profile'),
    path('task/', views.view_task, name='user-task'),
    path('request/', views.view_request, name='user-request'),
    path('attendance/', views.view_attendance, name='user-attendance')
]
