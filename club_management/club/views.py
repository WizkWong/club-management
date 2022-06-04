from django.shortcuts import render
from users.models import User_request

# from django.http import HttpResponse

posts = [
    {
        'author': 'User',
        'title': 'Test1',
        'content': 'First post',
        'date_posted': 'March 31, 2022'
    },
    {
        'author': 'User',
        'title': 'Test2',
        'content': 'Second post',
        'date_posted': 'April 1, 2022'
    }
]


def home(request):
    context = {
        'profile': posts,
        'title': 'Home',
        'pending_requests': [r for r in User_request.objects.all() if r.request_feedback.approval == r.request_feedback.PENDING]
    }
    return render(request, 'club/home.html', context)


def about(request):
    context = {
        'post': posts,
        'title': 'About'
    }
    return render(request, 'club/about.html', context)


