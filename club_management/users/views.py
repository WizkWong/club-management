from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
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
            print(user)
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
    return render(request, 'users/profile.html', {'title': 'Your Profile'})
