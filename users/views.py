from logging import raiseExceptions

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import RegistrationForm, LoginForm, ProfileEditForm
from django.conf import settings
from .models import Profile
import json

def home(request):
    return render(request, 'home.html')  # home HTML template

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()  # creating the user

            # profile creation is handled by the signal, so no need to manually create the profile here
            profile = user.profile  # fetching the profile created by the signal
            profile.save()  # saving the profile with the additional data

            return redirect('success')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('songs')
            else:
                return redirect('invalid_login')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def invalid_login(request):
    return render(request, 'invalid_login.html')

def song_view(request):
    # Pass the API key from settings to template
    api_key = settings.SPOTIFY_API_KEY # Spotify API key
    user = Profile.objects.get(user=request.user)
    return render(request, 'songs.html', {'api_key': api_key})

def registration_successful(request):
    return render(request, 'registration_successful.html')

@login_required(login_url='login')
def favorites(request):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        user = Profile.objects.get(user=request.user)
        user.save()
        return user
    if request.method == 'GET':
        user = Profile.objects.get(user=request.user)
        api_key = settings.SPOTIFY_API_KEY

        return render(request, 'songs.html', {"api_key": api_key})
    return render(request, 'songs.html')


@login_required(login_url='login')
def profile(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'profile.html', {'profile': user_profile})

def edit_profile(request, username):
    user = request.user
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = ProfileEditForm(instance=user)
    return render(request, 'edit_profile.html', {'form':form, 'additional_form':additional_form})

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email)
            if user.exists():
                token = PasswordResetTokenGenerator
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(f'/reset/{uid}/{token}/')
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                send_mail(
                    "password_reset_subject.txt",
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                )
                return render(request, 'password_reset_done.html')
            else:
                return redirect("user_doesnt_exist")
        else:
            form = PasswordResetForm()
        return render(request, 'password_reset.html', {'form': form})

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    return render(request, 'password_reset_confirm.html')

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')

def user_doesnt_exist(request):
    return render(request, 'user_doesnt_exist.html')  # user does not exist template

def songs_view(request):
    return render(request, 'songs.html')
