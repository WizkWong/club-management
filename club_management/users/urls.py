from django.urls import path
from . import views
from .views import (
    RequestListView,
    RequestDetailView,
    RequestCreateView,
    RequestDeleteView
)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profile, name='user-profile'),
    path('task/', views.view_task, name='user-task'),
    path('request/', RequestListView.as_view(), name='user-request'),
    path('request/<int:pk>/', RequestDetailView.as_view(), name='user-request-detail'),
    path('request/create/', RequestCreateView.as_view(), name='user-request-create'),
    path('request/<int:pk>/delete/', RequestDeleteView.as_view(), name='user-request-delete'),
    path('attendance/', views.view_attendance, name='user-attendance')
]
