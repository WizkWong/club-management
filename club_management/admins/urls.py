from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.manage_attendance, name='admin-attendance'),
    path('task/', views.manage_task, name='admin-task'),
    path('users/', views.manage_user, name='admin-user'),
    path('users/add/', views.add_user, name='admin-user-add'),
    path('users/<str:pk>/', views.edit_user, name='admin-user-edit'),
    path('users/<str:pk>/change_password/', views.change_password, name='admin-user-password'),
    path('users/<str:pk>/delete/', views.delete_user, name='admin-user-delete'),
    path('request/<str:types>/', views.manage_request, name='admin-request'),
    path('request/<str:types>/<int:pk>/', views.view_request_detail, name='admin-request-detail'),
    path('request/<str:types>/<int:pk>/delete', views.delete_request, name='admin-request-delete'),
    path('report/', views.manage_report, name='admin-report'),
    path('edit_page/', views.edit_page, name='admin-edit-page'),
]