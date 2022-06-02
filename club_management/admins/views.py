from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm
from users.models import User_request, Task_assigned
from .models import Request_feedback, Event, Task, Attendance_of_user
from .forms import RequestFeedbackForm, TaskForm
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .method import Percentage


def permission(request):
    if request.user.is_superuser is False:
        raise Http404("Page Not Found")


@login_required
def manage_attendance(request):
    permission(request)
    events = Event.objects.all().order_by('-datetime_created')
    attendance = []
    for event in events:
        n = [att.attendance for att in Attendance_of_user.objects.filter(event=event.id)]
        attendance.append(Percentage(len(n) - n.count(Attendance_of_user.ABSENT), len(n)))
    content = {
        'title': 'Manage Attendance',
        'events': zip(events, attendance)
    }
    return render(request, 'admins/attendance.html', content)


@login_required
def edit_attendance(request, pk):
    event = get_object_or_404(Event, id=pk)
    permission(request)
    content = {
        'title': 'Manage Attendance',
        'attendance_of_users': Attendance_of_user.objects.filter(event=event)
    }
    return render(request, 'admins/attendance.html', content)


@login_required
def manage_task(request):
    permission(request)
    tasks = Task.objects.all().order_by('-datetime_created')
    number_completion = []
    for task in tasks:
        n = [user_task.complete for user_task in Task_assigned.objects.filter(task=task.id)]
        number_completion.append(Percentage(n.count(True), len(n)))

    content = {
        'title': 'Manage Task',
        'tasks': zip(tasks, number_completion)
    }
    return render(request, 'admins/manage task/task.html', content)


@login_required
def create_task(request):
    permission(request)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            user_list = [User.objects.get(id=user_id) for user_id in request.POST.getlist('users')]
            for user in user_list:
                Task_assigned.objects.create(task=task, user=user)
            messages.success(request, 'New Task Created')
            return redirect('admin-task')

    else:
        form = TaskForm()

    content = {
        'title': 'Manage Task',
        'form': form,
        'all_user': User.objects.filter(is_superuser=False)
    }
    return render(request, 'admins/manage task/create task.html', content)


@login_required
def view_task_detail(request, pk):
    permission(request)
    task = get_object_or_404(Task, id=pk)

    content = {
        'title': 'Manage Task',
        'task': task,
        'assign_users': Task_assigned.objects.filter(task=task)
    }
    return render(request, 'admins/manage task/task detail.html', content)


@login_required
def edit_task_detail(request, pk):
    permission(request)
    task = get_object_or_404(Task, id=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task title:{task.title} is updated')
            return redirect('admin-task-detail', pk=pk)

    else:
        form = TaskForm(instance=task)

    content = {
        'title': 'Manage Task',
        'form': form,
        'task': task,
    }
    return render(request, 'admins/manage task/edit task detail.html', content)


@login_required
def delete_task_detail(request, pk):
    permission(request)
    task = get_object_or_404(Task, id=pk)

    if request.method == 'POST':
        for user_task in Task_assigned.objects.filter(task=task):
            user_task.delete()
        Task.objects.get(id=pk).delete()
        messages.success(request, f'{task.title} request is successfully delete!')
        return redirect('admin-task')

    content = {
        'title': 'Manage Task',
        'task': task,
    }
    return render(request, 'admins/manage task/delete task.html', content)


@login_required
def manage_user(request):
    permission(request)
    search = request.GET.get('search') if request.GET.get('search') is not None else ''
    content = {
        'title': 'Manage User',
        'all_user': User.objects.filter(is_superuser=False).filter(username__startswith=search),
        'search': search
    }
    return render(request, 'admins/manage user/view_user.html', content)


@login_required
def edit_user(request, pk):
    permission(request)
    user = get_object_or_404(User, Q(is_superuser=False), username=pk)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('admin-user')

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    content = {
        'title': 'Manage User',
        'u_form': u_form,
        'p_form': p_form,
        'username': pk
    }

    return render(request, 'admins/manage user/edit user.html', content)


@login_required
def change_password(request, pk):
    permission(request)
    user = get_object_or_404(User, Q(is_superuser=False), username=pk)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)

        if form.is_valid():
            user_pss = form.save()
            update_session_auth_hash(request, user_pss)
            messages.success(request, f'Account {pk} password was successfully change!')
            return redirect('admin-user')

    else:
        form = PasswordChangeForm(user)

    content = {
        'title': 'Change User Password',
        'form': form,
        'username': pk
    }
    return render(request, 'admins/manage user/change user password.html', content)


@login_required
def add_user(request):
    permission(request)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username}!')
            return redirect('admin-user')
    else:
        form = UserRegisterForm()

    content = {
        'title': 'Add User',
        'form': form
    }

    return render(request, 'admins/manage user/add user.html', content)


@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, Q(is_superuser=False), username=pk)
    permission(request)
    if request.method == 'POST':
        User.objects.get(username=user.username).delete()
        messages.success(request, f'{user.username} account is successfully delete!')
        return redirect('admin-user')

    content = {
        'title': 'Delete User',
        'username': user.username
    }

    return render(request, 'admins/manage user/delete user.html', content)


@login_required
def manage_request(request, types):
    permission(request)
    search = request.GET.get('search') if request.GET.get('search') is not None else ''
    objects = User_request.objects.filter(title__icontains=search).order_by('-datetime_created')

    if types == 'all':
        requests = objects

    elif types == 'pending':
        requests = [r for r in objects if r.request_feedback.approval == Request_feedback.PENDING]

    elif types == 'accept':
        requests = [r for r in objects if r.request_feedback.approval == Request_feedback.ACCEPT]

    elif types == 'reject':
        requests = [r for r in objects if r.request_feedback.approval == Request_feedback.REJECT]

    else:
        raise Http404("Page not found")

    content = {
        'title': 'Manage Request',
        'type': types,
        'requests': requests,
        'search': search
    }
    return render(request, 'admins/manage request/user request.html', content)


@login_required
def view_request_detail(request, types, pk):
    user_request = get_object_or_404(User_request, id=pk)
    permission(request)
    if request.method == 'POST':
        form = RequestFeedbackForm(request.POST, instance=user_request.request_feedback)

        if form.is_valid():
            form = form.save(commit=False)
            form.request_id = user_request.id
            form.user = request.user
            form.save()
            messages.success(request, f'Reply the request of Title: "{user_request.title}" successfully')
            return redirect('admin-request-detail', types=types, pk=pk)

    else:
        form = RequestFeedbackForm(instance=user_request.request_feedback)

    content = {
        'title': 'Manage Request',
        'request': user_request,
        'form': form,
        'type': types
    }
    return render(request, 'admins/manage request/user request detail.html', content)


@login_required
def delete_request(request, types, pk):
    user_request = get_object_or_404(User_request, id=pk)
    permission(request)
    if request.method == 'POST':
        User_request.objects.get(id=pk).delete()
        messages.success(request, f'{user_request.title} request is successfully delete!')
        return redirect('admin-request', types=types)

    content = {
        'title': 'Delete Request',
        'request': user_request,
        'type': types
    }

    return render(request, 'admins/manage request/delete request.html', content)


@login_required
def manage_report(request):
    permission(request)

    content = {
        'title': 'Manage Report',
        'events': Event.objects.all()
    }
    return render(request, 'admins/manage report/report.html', content)


@login_required
def edit_page(request):
    permission(request)
    content = {
        'title': 'Edit Page'
    }
    return render(request, 'admins/edit page.html', content)
