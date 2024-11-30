from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Wrap
from django.utils.translation import gettext_lazy as _

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    email = forms.EmailField(label=_("Email"))
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1', 'password2']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"))
    class Meta:
        model = User
        fields = ['username', 'password']

class FeedbackForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

class WrapSettingsForm(forms.Form):
    TIME_RANGE_CHOICES = [
        ('short_term', 'Last 4 Weeks'),
        ('medium_term', 'Last 6 Months'),
        ('long_term', 'Last year')
    ]
    time_range = forms.ChoiceField(choices=TIME_RANGE_CHOICES, label="Time Range")
    limit = forms.IntegerField(min_value=1, max_value=50, initial=10, label="Number of Items")


class WrapForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Wrap
        fields = ['title', 'top_artists', 'top_tracks']
