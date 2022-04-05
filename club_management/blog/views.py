from django.shortcuts import render
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

data = [
    'Bing', 'Google', 'Firefox'
]


def home(request):
    context = {
        'profile': posts,
        'title': 'home'
    }
    return render(request, 'blog/home.html', context)

def about(request):
    context = {
        'types': data
    }
    return render(request, 'blog/about.html', context)
