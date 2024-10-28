# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('spotify_login/', views.spotify_login, name='spotify_login'),
    path('callback/', views.spotify_callback, name='spotify_callback'),
    path('spotify_data/', views.spotify_data, name='spotify_data'),
    path('spotify_logout/', views.spotify_logout, name='spotify_logout'),  # Add this line

]
