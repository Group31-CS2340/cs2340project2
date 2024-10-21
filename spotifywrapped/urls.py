"""
URL configuration for spotifywrapped project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
path('', user_views.home, name='home'),
    path("register/", user_views.register, name='register'),
    path("success/", user_views.registration_successful, name='success'),
    path('login/', user_views.login_view, name='login'),
    path('invalid_login/', user_views.invalid_login, name='invalid_login'),
    path('profile/<str:username>/', user_views.profile, name='profile'),
    path('edit-profile/<str:username>/', user_views.edit_profile, name='edit-profile'),
    # password reset views
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='templates/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='templates/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='templates/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='templates/password_reset_complete.html'),
         name='password_reset_complete'),
    # password change views
    path('password-change/',
         auth_views.PasswordChangeView.as_view(template_name='templates/password_change.html'),
         name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='templates/password_change_done.html'),
         name='password_change_done'),
    # path('user-doesnt-exist/', )
]