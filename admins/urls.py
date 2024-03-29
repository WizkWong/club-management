from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.manage_attendance, name='admin-attendance'),
    path('attendance/<int:pk>/', views.edit_attendance, name='admin-attendance-edit'),
    path('task/', views.manage_task, name='admin-task'),
    path('task/create/', views.create_task, name='admin-task-create'),
    path('task/<int:pk>/', views.view_task_detail, name='admin-task-detail'),
    path('task/<int:pk>/edit/', views.edit_task_detail, name='admin-task-detail-edit'),
    path('task/<int:pk>/delete/', views.delete_task_detail, name='admin-task-detail-delete'),
    path('users/', views.manage_user, name='admin-user'),
    path('users/add/', views.add_user, name='admin-user-add'),
    path('users/<str:pk>/', views.edit_user, name='admin-user-edit'),
    path('users/<str:pk>/change_password/', views.change_password, name='admin-user-password'),
    path('users/<str:pk>/delete/', views.delete_user, name='admin-user-delete'),
    path('request/<str:types>/', views.manage_request, name='admin-request'),
    path('request/<str:types>/<int:pk>/', views.view_request_detail, name='admin-request-detail'),
    path('request/<str:types>/<int:pk>/delete/', views.delete_request, name='admin-request-delete'),
    path('report/', views.manage_report, name='admin-report'),
    path('report/generate:<int:pk>/', views.generate_report, name='admin-report-generate'),
    path('edit_page/home/', views.edit_home_page, name='admin-edit-home-page'),
    path('edit_page/about/', views.edit_about_page, name='admin-edit-about-page'),
    path('event/', views.manage_event, name='admin-event'),
    path('event/create/', views.create_event, name='admin-event-create'),
    path('event/<int:pk>/modify/', views.modify_event, name='admin-event-modify'),
    path('event/<int:pk>', views.view_event, name='admin-event-detail'),
    path('event/<int:pk>/delete', views.delete_event, name='admin-event-delete'),
]