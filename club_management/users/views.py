from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserRequestForm
from .models import User_request
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404


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

    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})


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

    return render(request, 'users/login.html', {'form': form, 'title': 'Login'})


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
        'title': 'Your Profile',
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def view_task(request):
    permission(request, request.user)
    content = {
        'title': 'User Task'
    }
    return render(request, 'users/task/task.html', content)


@login_required
def view_request(request):
    permission(request, request.user)
    content = {
        'title': 'request',
        'requests': User_request.objects.filter(user=request.user)
    }
    return render(request, 'users/request/view request.html', content)


@login_required
def view_request_detail(request, pk):
    user_request = get_object_or_404(User_request, id=pk)
    permission(request, user_request.user)
    content = {
        'title': 'request',
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
        'title': 'request',
        'form': form
    }
    return render(request, 'users/request/create request.html', content)


@login_required
def delete_request(request, pk):
    user_request = get_object_or_404(User_request, id=pk)
    permission(request, user_request.user)
    if request.method == 'POST':
        User_request.objects.filter(id=pk).delete()
        messages.success(request, f'{user_request.title} request is successfully delete!')
        return redirect('user-request')

    content = {
        'title': 'request',
        'request': user_request
    }
    return render(request, 'users/request/delete request.html', content)


@login_required
def view_attendance(request):
    permission(request, request.user)
    content = {
        'title': 'User Attendance'
    }
    return render(request, 'users/attendance.html', content)


# class RequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
#     model = User_request
#     template_name = 'users/request/view request.html'
#     context_object_name = 'requests'
#     ordering = ['-datetime_created']
#
#     def get_queryset(self):
#         return User_request.objects.filter(user=self.request.user)
#
#     def test_func(self):
#         if self.request.user.is_superuser:
#             return False
#         return True
#
#
# class RequestDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = User_request
#     template_name = 'users/request/view request detail.html'
#     context_object_name = 'request'
#
#     def test_func(self):
#         request = self.get_object()
#         if self.request.user.is_superuser or self.request.user != request.user:
#             return False
#         return True
#
#
# class RequestCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = User_request
#     template_name = 'users/request/create request.html'
#     fields = ['title', 'detail']
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#
#     def test_func(self):
#         if self.request.user.is_superuser:
#             return False
#         return True
#
#
# class RequestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = User_request
#     template_name = 'users/request/delete request.html'
#     success_url = '/request/'
#
#     def test_func(self):
#         request = self.get_object()
#         if self.request.user.is_superuser or self.request.user != request.user:
#             return False
#         return True
