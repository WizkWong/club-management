from django.shortcuts import render
from users.models import User_request
from club_management.settings import MEDIA_URL
# from django.http import HttpResponse


def title():
    with open(f'{MEDIA_URL.replace("/", "")}/page/title.txt', 'r') as f:
        return f.read().strip()


def home(request):
    title()
    paragraph1 = 'CSS will display overflow in this way, because doing something else could cause data loss. In CSS data loss means that some of your content vanishes. So the initial value of overflow is visible, and we can see the overflowing text. It is generally better to be able to see overflow, even if it is messy. If things were to disappear or be cropped as would happen if overflow was set to hidden you might not spot it when previewing your site. Messy overflow is at least easy to spot, and in the worst case, your visitor will be able to see and read the content even if it looks a bit strange.'
    paragraph2 = 'CSS will display overflow in this way, because doing something else could cause data loss. In CSS data loss means that some of your content vanishes. So the initial value of overflow is visible, and we can see the overflowing text. It is generally better to be able to see overflow, even if it is messy. If things were to disappear or be cropped as would happen if overflow was set to hidden you might not spot it when previewing your site. Messy overflow is at least easy to spot, and in the worst case, your visitor will be able to see and read the content even if it looks a bit strange.'
    context = {
        'title': 'Home',
        'title_page': title(),
        'top_background': 'page/default-top-background.jpg',
        'image': 'page/home picture.jpg',
        'title_text': 'Welcome',
        'paragraph1': paragraph1,
        'paragraph2': paragraph2,
        'paragraph3': None,
    }
    if request.user.is_superuser:
        context.update({'pending_requests': [r for r in User_request.objects.all() if r.request_feedback.approval == r.request_feedback.PENDING]})

    return render(request, 'club/home.html', context)


def about(request):
    context = {
        'title': 'About',
        'title_page': title(),
        'top_background': 'page/default-top-background.jpg',
        'paragraph': None,
    }
    return render(request, 'club/about.html', context)


