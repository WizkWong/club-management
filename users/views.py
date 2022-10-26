from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserRequestForm, TaskSubmissionForm
from .models import User_request, Task_assigned
from admins.models import Attendance_of_user, Event, Page
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils import timezone
from admins.method import Attendance_code as Atd_code
from django.db.models import Q


def permission(request, user):
    if request.user.is_superuser is True or request.user != user:
        raise Http404("Permission denied")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('club-home')
    else:
        form = UserRegisterForm()

    content = {
        'title': 'Register',
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'form': form,
    }
    return render(request, 'users/register.html', content)


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("club-home")
            else:
                messages.error(request, "Invalid username or passwordss.")

        else:
            messages.error(request, "Invalid username or password")

    else:
        form = AuthenticationForm()

    content = {
        'title': 'Login',
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'form': form,
    }
    return render(request, 'users/login.html', content)


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("club-home")


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('user-profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user_pss = form.save()
            update_session_auth_hash(request, user_pss)
            messages.success(request, f'Your account password was successfully change!')
            return redirect('user-profile')

    else:
        form = PasswordChangeForm(request.user)

    content = {
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'form': form,
    }
    return render(request, 'users/change password.html', content)


@login_required
def view_task(request):
    permission(request, request.user)
    tasks = Task_assigned.objects.filter(user=request.user).order_by('-task')
    content = {
        'title': 'User Task',
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'tasks': tasks,
    }
    return render(request, 'users/task/task.html', content)


@login_required
def submit_task(request, pk):
    permission(request, request.user)
    task = get_object_or_404(Task_assigned, Q(user=request.user), task=pk)
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form = form.save(commit=False)
            form.complete = True
            form.datetime_complete = timezone.now()
            form.save()
            messages.success(request, f'{task.task.title} task is submitted')
            return redirect('submit-task', pk)
    else:
        form = TaskSubmissionForm(instance=task)

    content = {
        'title': 'User Task',
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'task': task,
        'form': form,
    }
    return render(request, 'users/task/submit task.html', content)


@login_required
def view_request(request):
    permission(request, request.user)
    content = {
        'title': 'User Request',
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'requests': User_request.objects.filter(user=request.user).order_by('-datetime_created')
    }
    return render(request, 'users/request/view request.html', content)


@login_required
def view_request_detail(request, pk):
    user_request = get_object_or_404(User_request, id=pk)
    permission(request, user_request.user)
    content = {
        'title': 'User Request',
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'request': user_request
    }
    return render(request, 'users/request/view request detail.html', content)


@login_required
def create_request(request):
    permission(request, request.user)
    if request.method == 'POST':
        form = UserRequestForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Your request has been created')
            return redirect('user-request')

    else:
        form = UserRequestForm()

    content = {
        'title': 'User Request',
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'form': form
    }
    return render(request, 'users/request/create request.html', content)


@login_required
def delete_request(request, pk):
    user_request = get_object_or_404(User_request, id=pk)
    permission(request, user_request.user)
    if request.method == 'POST':
        User_request.objects.get(id=pk).delete()
        messages.success(request, f'{user_request.title} request is successfully delete!')
        return redirect('user-request')

    content = {
        'title': 'User Request',
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'request': user_request
    }
    return render(request, 'users/request/delete request.html', content)


@login_required
def view_attendance(request):
    permission(request, request.user)
    code = request.GET.get('code')

    if code is not None:
        event = Atd_code.check(int(code))
        if event is None:
            messages.error(request, 'This code does not exist')
        else:
            if Attendance_of_user.objects.filter(event=event, user=request.user).exists():
                atd = Attendance_of_user.objects.get(event=event, user=request.user)
                if atd.attendance == Attendance_of_user.ABSENT:
                    atd.attendance = Attendance_of_user.PRESENT
                    atd.save()
                    messages.success(request, f'Successfully taken attendance from {event.title}')
                else:
                    messages.error(request, f'You have already taken the attendance from {event.title}')

            else:
                messages.error(request, f'Your Attendance is not exist. Reason: Created account before Attendance created')

    user_atd = [atd for atd in Attendance_of_user.objects.filter(user=request.user).order_by("event")
                if atd.attendance != Attendance_of_user.ABSENT]
    content = {
        'title': 'User Attendance',
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'user_attendance': user_atd,
    }
    return render(request, 'users/attendance.html', content)


def view_event(request):
    search = request.GET.get('search') if request.GET.get('search') is not None else ''

    content = {
        'title': 'Event',
        'title_page': Page.objects.first().title_page if Page.objects.first().title_page else '',
        'events': Event.objects.filter(title__icontains=search).order_by('-datetime_created')
    }
    return render(request, 'users/event.html', content)

