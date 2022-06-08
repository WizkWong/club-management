from django import forms
from .models import Request_feedback, Task, Page


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class RequestFeedbackForm(forms.ModelForm):
    feedback = forms.CharField(required=False,
                               widget=forms.Textarea(
                                   attrs={
                                       "rows": 10,
                                       "cols": 70,
                                       "class": "field"
                                   }
                               ))

    class Meta:
        model = Request_feedback
        fields = ['approval', 'feedback']


class TaskForm(forms.ModelForm):
    detail = forms.CharField(required=False,
                             widget=forms.Textarea(
                                 attrs={
                                     "rows": 10,
                                     "cols": 70,
                                     "class": "field"
                                 }
                             ))

    class Meta:
        model = Task
        fields = ['title', 'detail', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'size': 60}),
            'deadline': DateTimePickerInput(),
        }


class EditHomePageForm(forms.ModelForm):
    title_page = forms.CharField(required=False)
    phone_number = forms.IntegerField(required=False)
    email = forms.EmailField(required=False)
    title_text = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': 163, "placeholder": "Title..."}))
    paragraph1 = forms.CharField(required=False,
                                 widget=forms.Textarea(
                                     attrs={
                                         "placeholder": " Paragraph...",
                                         "rows": 10,
                                         "cols": 150,
                                         "class": "field"
                                     }
                                 ))
    paragraph2 = forms.CharField(required=False,
                                 widget=forms.Textarea(
                                     attrs={
                                         "placeholder": " Paragraph...",
                                         "rows": 12,
                                         "cols": 85,
                                         "class": "field"
                                     }
                                 ))
    paragraph3 = forms.CharField(required=False,
                                 widget=forms.Textarea(
                                     attrs={
                                         "placeholder": " Paragraph...",
                                         "rows": 10,
                                         "cols": 150,
                                         "class": "field"
                                     }
                                 ))
    top_background = forms.ImageField(required=False, widget=forms.FileInput())
    image = forms.ImageField(required=False, widget=forms.FileInput())

    class Meta:
        model = Page
        fields = ['title_page', 'title_text', 'paragraph1', 'paragraph2', 'paragraph3',
                  'phone_number', 'email', 'top_background', 'image']


class EditAboutUsPageForm(forms.ModelForm):
    about_us = forms.CharField(required=False,
                               widget=forms.Textarea(
                                   attrs={
                                       "placeholder": " We Are ...",
                                       "rows": 20,
                                       "cols": 160,
                                       "class": "field"
                                   }
                               ))

    class Meta:
        model = Page
        fields = ['about_us']
