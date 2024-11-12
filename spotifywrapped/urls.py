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


from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.views.i18n import set_language

urlpatterns = [
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path("register/", user_views.register, name='register'),
    path("success/", user_views.registration_successful, name='success'),
    path('login/', user_views.login_view, name='login'),
    path('songs/', user_views.songs_view, name='songs'),
    path('invalid_login/', user_views.invalid_login, name='invalid_login'),
    path('profile/<str:username>/', user_views.profile, name='profile'),
    path('edit-profile/<str:username>/', user_views.edit_profile, name='edit-profile'),
    # password reset views
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    # password change views
    path('password-change/',
         auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),
    # path('user-doesnt-exist/', )
    path('delete-account/', user_views.delete_account, name='delete-account'),
    path('deleted', user_views.account_deleted, name='deleted'),
    path('logout/', user_views.logout_view, name='logout'),

    path('contact/', user_views.contact_view, name ='contact'),
    path('homepage', user_views.home_logged_in, name='home_logged_in'),
    path('explore', user_views.explore, name='explore'),
    path('public-profile/<str:username>/', user_views.public_profile, name='public_profile'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('new-wrap/', user_views.wrap_generate, name='new_wrap'),
    path('wrap/save/', user_views.save_wrap_to_profile, name='save_wrap_to_profile'),
    path('wrap/<int:wrap_id>/', user_views.wrap_detail, name='wrap_detail'),
]
