from django.shortcuts import render
from users.models import User_request
from admins.models import Page


def home(request):
    if Page.objects.first() is None:
        Page.objects.create()

    page = Page.objects.first()

    context = {
        'title': 'Home',
        'title_page': page.title_page if page.title_page else '',
        'top_background': page.top_background if page.top_background else 'page/default-top-background.jpg',
        'image': page.image if page.image else None,
        'title_text': page.title_text if page.title_text else '',
        'paragraph1': page.paragraph1 if page.paragraph1 else '',
        'paragraph2': page.paragraph2 if page.paragraph2 else '',
        'paragraph3': page.paragraph3 if page.paragraph3 else '',
        'phone_number': page.phone_number if page.phone_number else '',
        'email': page.email if page.email else '',
    }
    if request.user.is_superuser:
        context.update({'pending_requests': [r for r in User_request.objects.all() if
                                             r.request_feedback.approval == r.request_feedback.PENDING]})

    return render(request, 'club/home.html', context)


def about(request):
    page = Page.objects.first()

    context = {
        'title': 'About',
        'title_page': page.title_page if page.title_page else '',
        'top_background': page.top_background if page.top_background else 'page/default-top-background.jpg',
        'paragraph': page.about_us if page.about_us else '',
    }
    return render(request, 'club/about.html', context)
