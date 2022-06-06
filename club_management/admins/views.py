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
from django.utils import timezone
from django.http import FileResponse, HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle


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
    permission(request)
    event = get_object_or_404(Event, id=pk)

    if request.method == 'POST':
        for atd in Attendance_of_user.objects.filter(event=event):
            user = atd.user
            new_atd = int(request.POST.get(user.username))
            if atd.attendance == new_atd:
                continue
            else:
                Attendance_of_user.objects.filter(user=user.id).update(attendance=new_atd)

        messages.success(request, f"Attendance from '{event.title}' Event is save")

    content = {
        'title': 'Manage Attendance',
        'event': event,
        'attendance_of_users': Attendance_of_user.objects.filter(event=event),
        'present': Attendance_of_user.PRESENT,
        'absent': Attendance_of_user.ABSENT,
        'late': Attendance_of_user.LATE
    }
    return render(request, 'admins/edit attendance.html', content)


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
            user_list = [User.objects.get(id=user_id) for user_id in request.POST.getlist('users')]
            if len(user_list) == 0:
                messages.error(request, 'Please assign this task to at least one member')
            else:
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                for user in user_list:
                    Task_assigned.objects.create(task=task, user=user)
                messages.success(request, f'{task.title} Task is successfully created')
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
    permission(request)
    user = get_object_or_404(User, Q(is_superuser=False), username=pk)
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
    permission(request)
    user_request = get_object_or_404(User_request, id=pk)
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
    permission(request)
    user_request = get_object_or_404(User_request, id=pk)
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
    events = [e for e in Event.objects.all().order_by("-datetime_created") if e.end_time < timezone.now()]

    content = {
        'title': 'Manage Report',
        'events': events
    }
    return render(request, 'admins/manage report/report.html', content)


@login_required
def generate_report(request, pk):
    permission(request)
    event = get_object_or_404(Event, id=pk)
    user_attendance = Attendance_of_user.objects.filter(event=event.id).order_by("-user")
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    # Add lines of text
    lines = [
        f'{event.title}',
        f'{event.detail}',
        f'{event.start_time}',
        f'{event.end_time}',
    ]

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()

    data = []

    # 23
    n = 0
    for x in range(0, 100):
        for atd in user_attendance:
            user = f'{atd.user.username.strip()}\n'
            if atd.attendance == Attendance_of_user.PRESENT:
                data.append([user, 'Present\n'])

            elif atd.attendance == Attendance_of_user.ABSENT:
                data.append([user, 'Absent\n'])

            elif atd.attendance == Attendance_of_user.LATE:
                data.append([user, 'Late\n'])

            if n == 23:
                c.showPage()
                n = 0

            else:
                n += 1

    data.append(['Member\n', 'Attendance\n'])

    t = Table(data, colWidths=250)
    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                           ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])),

    t.wrapOn(c, 500, len(data) * 100)
    t.drawOn(c, 60, 40)

    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=False, filename=f'{event.title}_report.pdf')


@login_required
def edit_page(request):
    permission(request)
    content = {
        'title': 'Edit Page'
    }
    return render(request, 'admins/edit page.html', content)
