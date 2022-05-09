from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def manage_attendance(request):
    content = {
        'title': 'Manage Attendance'
    }
    return render(request, 'admins/attendance.html', content)


@login_required
def manage_task(request):
    content = {
        'title': 'Manage Task'
    }
    return render(request, 'admins/task.html', content)


@login_required
def manage_user(request):
    content = {
        'title': 'Manage User'
    }
    return render(request, 'admins/user.html', content)


@login_required
def manage_request(request):
    content = {
        'title': 'Manage Request'
    }
    return render(request, 'admins/request.html', content)


@login_required
def manage_report(request):
    content = {
        'title': 'Manage Report'
    }
    return render(request, 'admins/report.html', content)


@login_required
def edit_page(request):
    content = {
        'title': 'Edit Page'
    }
    return render(request, 'admins/edit page.html', content)
