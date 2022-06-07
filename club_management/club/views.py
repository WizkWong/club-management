from django.shortcuts import render
from users.models import User_request
from club_management.settings import MEDIA_URL
import os


def read_file(filename):
    if os.path.exists(f'{MEDIA_URL.replace("/", "")}/page/{filename}'):
        with open(f'{MEDIA_URL.replace("/", "")}/page/{filename}', 'r') as f:
            return f.read().strip()

    else:
        f = open(f'{MEDIA_URL.replace("/", "")}/page/{filename}', "x")
        f.close()
        return None


def home(request):
    context = {
        'title': 'Home',
        'title_page': read_file('title_page.txt'),
        'top_background': read_file('top_background.txt') if len(read_file('top_background.txt')) != 0
        else 'page/default-top-background.jpg',
        'image': read_file('home_picture.txt'),
        'title_text': read_file('title_text.txt'),
        'paragraph1': read_file('paragraph1.txt'),
        'paragraph2': read_file('paragraph2.txt'),
        'paragraph3': read_file('paragraph3.txt'),
        'phone_number': read_file('phone_number.txt'),
        'email': read_file('email.txt'),
    }
    if request.user.is_superuser:
        context.update({'pending_requests': [r for r in User_request.objects.all() if
                                             r.request_feedback.approval == r.request_feedback.PENDING]})

    return render(request, 'club/home.html', context)


def about(request):
    context = {
        'title': 'About',
        'title_page': read_file('title_page.txt'),
        'top_background': read_file('top_background.txt') if len(read_file('top_background.txt')) != 0
        else 'page/default-top-background.jpg',
        'paragraph': read_file('about_us.txt'),
    }
    return render(request, 'club/about.html', context)
