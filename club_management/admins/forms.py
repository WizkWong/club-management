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
