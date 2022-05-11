from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.forms import UserUpdateForm, ProfileUpdateForm
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
    return render(request, 'admins/user.html', content)


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
        'p_form': p_form
    }

    return render(request, 'admins/user edit.html', content)



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
