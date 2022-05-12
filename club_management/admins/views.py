from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm
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
    return render(request, 'admins/task.html', content)


@login_required
def manage_user(request):
    permission(request)
    content = {
        'title': 'Manage User',
        'all_user': User.objects.filter(is_superuser=False)
    }
    return render(request, 'admins/manage user/user.html', content)


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


def change_password(request, pk):
    permission(request)
    user = get_object_or_404(User, Q(is_superuser=False), username=pk)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)

        if form.is_valid():
            user_pss = form.save()
            update_session_auth_hash(request, user_pss)
            messages.success(request, 'Your password was successfully updated!')
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
        messages.success(request, f'{pk} account are successfully delete!')
        return redirect('admin-user')

    content = {
        'title': 'Delete User',
        'username': pk
    }

    return render(request, 'admins/manage user/delete user.html', content)



@login_required
def manage_request(request):
    permission(request)
    content = {
        'title': 'Manage Request'
    }
    return render(request, 'admins/request.html', content)


@login_required
def manage_report(request):
    permission(request)
    content = {
        'title': 'Manage Report'
    }
    return render(request, 'admins/report.html', content)


@login_required
def edit_page(request):
    permission(request)
    content = {
        'title': 'Edit Page'
    }
    return render(request, 'admins/edit page.html', content)
