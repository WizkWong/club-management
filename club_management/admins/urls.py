from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.manage_attendance, name='admin-attendance'),
    path('task/', views.manage_task, name='admin-task'),
    path('all_users/', views.manage_user, name='admin-user'),
    path('all_users/add', views.add_user, name='admin-user-add'),
    path('all_users/<str:pk>', views.edit_user, name='admin-user-edit'),
    path('all_users/<str:pk>/change_password', views.change_password, name='admin-user-password'),
    path('all_users/<str:pk>/delete', views.delete_user, name='admin-user-delete'),
    path('request/', views.manage_request, name='admin-request'),
    path('report/', views.manage_report, name='admin-report'),
    path('edit_page/', views.edit_page, name='admin-edit-page'),
]