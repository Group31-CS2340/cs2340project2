from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
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
    class Meta:
        model = User
        fields = ['username', 'password']

class FeedbackForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    
