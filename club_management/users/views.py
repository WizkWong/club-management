from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User


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


def view_task(request):
    content = {
        'title': 'User Task'
    }
    return render(request, 'users/task.html', content)


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
