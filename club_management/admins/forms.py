from django import forms
from .models import Request_feedback, Task


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


class EditHomePageForm(forms.Form):
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
                                         "rows": 13,
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
    top_background = forms.ImageField(required=False)
    home_picture = forms.ImageField(required=False)


class EditAboutUsPageForm(forms.Form):
    about_us = forms.CharField(required=False,
                               widget=forms.Textarea(
                                   attrs={
                                       "placeholder": " We Are ...",
                                       "rows": 20,
                                       "cols": 160,
                                       "class": "field"
                                   }
                               ))
