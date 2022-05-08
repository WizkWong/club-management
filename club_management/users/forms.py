from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(help_text='Required 6-30 character',
                               max_length=30,
                               min_length=6,
                               widget=forms.TextInput(attrs={'size': 20}))
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(help_text='Required 6-30 character',
                               max_length=30,
                               min_length=6,
                               widget=forms.TextInput(attrs={'size': 20}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'size': 35}))

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    description = forms.CharField(required=False,
                                  widget=forms.Textarea(
                                      attrs={
                                          "placeholder": "Your Description...",
                                          "rows": 10,
                                          "cols": 70,
                                          "class": "field"
                                      }
                                  ))

    class Meta:
        model = profile
        fields = ['description', 'image']
