from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm
from users.models import User_request
from .models import Request_feedback
from .forms import RequestFeedbackForm
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404
from django.db.models import Q


def permission(request):
    if request.user.is_superuser is False:
        raise Http404("Page Not Found")


@login_required
def manage_attendance(request):
    permission(request)
    content = {
        'title': 'Manage Attendance'
    }
    return render(request, 'admins/attendance.html', content)


@login_required
def manage_task(request):
    permission(request)
    content = {
        'title': 'Manage Task'
    }
    return render(request, 'admins/manage task/task.html', content)


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
            messages.success(request, f'Account {user.username} password was successfully change!')
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
        User.objects.filter(username=user.username).delete()
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
    objects = User_request.objects.all().filter(title__icontains=search).order_by('-datetime_created')

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
            messages.success(request, f'Reply the request of Title:"{user_request.title}" successfully')
            return redirect('admin-request', types=types)

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
        User_request.objects.filter(id=pk).delete()
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
        'title': 'Manage Report'
    }
    return render(request, 'admins/manage report/report.html', content)


@login_required
def edit_page(request):
    permission(request)
    content = {
        'title': 'Edit Page'
    }
    return render(request, 'admins/edit page.html', content)
