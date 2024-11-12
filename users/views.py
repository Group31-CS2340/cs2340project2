import time
from logging import raiseExceptions

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from django.views.decorators.cache import never_cache

from .forms import RegistrationForm, LoginForm, ProfileEditForm, FeedbackForm, WrapForm
from django.conf import settings
from .models import Profile, Feedback, Wrap
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import logout


import json
import webbrowser
from urllib.parse import urlencode
import base64
import requests

def home(request):
    if request.user.is_authenticated:
        return redirect('home_logged_in')
    return render(request, 'home.html')# home HTML template

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
                return redirect('home_logged_in')
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
    return render(request, 'edit_profile.html', {'form':form,})

def public_profile(request, username):
    user = request.user
    profile = request.user.profile
    return render(request, 'public_profile.html', {'user': user, 'profile': profile})

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

def contact_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Save the feedback to the database
            Feedback.objects.create(
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Your feedback has been submitted successfully.')
            return redirect('contact')
        else:
            messages.error(request, 'There was an error with your submission. Please try again.')
    else:
        form = FeedbackForm()
    return render(request, 'contact.html', {'form': form})

    

def delete_account(request):
        user = request.user
        user.delete()
        return redirect('deleted')

def account_deleted(request):
    return render(request, 'account_deleted.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def home_logged_in(request):
    user_wraps = Wrap.objects.filter(user=request.user).order_by('-created_at')  # Ensure Wrap model has a created_at field
    return render(request, 'logged_in_home.html', {'wraps': user_wraps})


def explore(request):
    return render(request, 'explore.html')




def spotify_login(request):
    request.session.flush()  # Clear any existing session data
    print("Session cleared in spotify_login")  # Debug: Confirm session flush
    cleanup()
    client_id = settings.SPOTIFY_CLIENT_ID
    auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
    "scope": "user-top-read"
    }

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

    return redirect("spotify_data")

# users/views.py
def spotify_callback(request):
    spotifyToken = request.session.get('spotify_token', None)
    code = request.GET.get('code')
    if not spotifyToken and code:
        client_id = settings.SPOTIFY_CLIENT_ID
        client_secret = settings.SPOTIFY_CLIENT_SECRET

        encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

        token_headers = {
            "Authorization": "Basic " + encoded_credentials,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI
        }

        r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
        token = r.json()["access_token"]
        request.session["spotify_token"] = token
    return redirect('users:spotify_data')


from django.views.decorators.cache import never_cache

@never_cache
def spotify_data(request):
    token = request.session.get('spotify_token')
    if not token:
        return redirect('users:spotify_login')
    
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    user_params = {
        "limit": 10,
        "time_range": "short_term"
    }

    # Fetch the most recent data from Spotify
    try:
        top_artists = requests.get("https://api.spotify.com/v1/me/top/artists", params=user_params, headers=user_headers)
        top_tracks = requests.get("https://api.spotify.com/v1/me/top/tracks", params=user_params, headers=user_headers)
    except Exception as e:
        print("Error fetching data in spotify_data:", e)
        # return redirect('users:spotify_login')

    return render(request, 'users/spotify_data.html', {
        'top_artists': top_artists.json(),
        'top_tracks': top_tracks.json()
    })

from .forms import WrapSettingsForm

@login_required()
def wrap_generate(request):
    token = request.session.get('spotify_token')
    if not token:
        return redirect('users:spotify_login')

    if request.method == 'POST':
        form = WrapSettingsForm(request.POST)
        if form.is_valid():
            time_range = form.cleaned_data['time_range']
            limit = form.cleaned_data['limit']
    else:
        form = WrapSettingsForm()
        time_range = 'short_term'
        limit = 10

    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    user_params = {
        "limit": limit,
        "time_range": time_range
    }

    # Fetch the most recent data from Spotify
    try:
        top_artists = requests.get("https://api.spotify.com/v1/me/top/artists", params=user_params,
                                   headers=user_headers)
        top_tracks = requests.get("https://api.spotify.com/v1/me/top/tracks", params=user_params, headers=user_headers)
    except Exception as e:
        print("Error fetching data in spotify_data:", e)
        # return redirect('users:spotify_login')

    top_artists_data = top_artists.json()
    top_tracks_data = top_tracks.json()

    return render(request, 'users/newWrap.html', {
        'top_artists': top_artists_data,
        'top_tracks': top_tracks_data,
        'form': form
    })

def save_wrap_to_profile(request):
    if request.method == "POST":
        # Get wrap data and title from the form
        title = request.POST.get("title", "My Spotify Wrap")  # Default title if empty
        top_artists_data = request.session.get("top_artists")
        top_tracks_data = request.session.get("top_tracks")

        if not top_artists_data or not top_tracks_data:
            return redirect('new_wrap')  # Redirect to generate if no data available

        # Save wrap to profile with the provided title
        wrap = Wrap.objects.create(
            user=request.user,
            title=title,
            top_artists=top_artists_data,
            top_tracks=top_tracks_data
        )
        return redirect('profile')  # Redirect to the profile or wraps list page
    else:
        return redirect('home')

def wrap_detail(request, wrap_id):
    wrap = get_object_or_404(Wrap, id=wrap_id)
    return render(request, 'wrap_detail.html', {'wrap': wrap})

# users/views.py
from django.contrib.auth import logout

# users/views.py
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


from django.shortcuts import redirect

def spotify_logout(request):
    print("Clearing session data in spotify_logout")  # Debug
    request.session.pop('spotify_token', None)
    request.session.flush()  # Ensure all session data is cleared
    response = redirect('users:spotify_login')
    response.delete_cookie('sessionid')
    print("Session and cookies cleared in spotify_logout")  # Debug
    time.sleep(3)
    return response

import os

def cleanup():
    # Locate and remove any .cache files created by SpotifyOAuth
    for filename in os.listdir():
        if filename.startswith(".cache"):
            os.remove(filename)
            print(f"Removed cache file: {filename}")
