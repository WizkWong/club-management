from django.urls import path
from . import views
# from .views import (
#     RequestListView,
#     RequestDetailView,
#     RequestCreateView,
#     RequestDeleteView
# )

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profile, name='user-profile'),
    path('task/', views.view_task, name='user-task'),
    path('request/', views.view_request, name='user-request'),
    path('request/<int:pk>/', views.view_request_detail, name='user-request-detail'),
    path('request/create/', views.create_request, name='user-request-create'),
    path('request/<int:pk>/delete/', views.delete_request, name='user-request-delete'),
    path('attendance/', views.view_attendance, name='user-attendance')
]
