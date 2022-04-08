from django.shortcuts import render
from .models import Post
# from django.http import HttpResponse

posts = [
    {
        'author': 'Chi Jian',
        'title': 'Test1',
        'content': 'First post',
        'date_posted': 'March 31, 2022'
    },
    {
        'author': 'Chi Jian',
        'title': 'Test2',
        'content': 'Second post',
        'date_posted': 'April 1, 2022'
    }
]

def home(request):
    context = {
        'profile': posts,
        'title': 'Home'
    }
    return render(request, 'club/home.html', context)

def about(request):
    context = {
        'post': Post.objects.all(),
        'title': 'About'
    }
    return render(request, 'club/about.html', context)
