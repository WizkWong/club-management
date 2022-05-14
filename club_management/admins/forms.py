from django import forms
from .models import Request_feedback


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
