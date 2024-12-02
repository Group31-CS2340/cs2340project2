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
from django.urls import path, include, reverse_lazy
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
     path('users/', include('users.urls')),
     path('admin/', admin.site.urls),
     path('', user_views.home, name='home'),
     path('register/', user_views.register, name='register'),
     path('success/', user_views.registration_successful, name='success'),
     path('login/', user_views.login_view, name='login'),
     path('invalid_login/', user_views.invalid_login, name='invalid_login'),
     path('profile/<str:username>/', user_views.profile, name='profile'),
     path('public-profile/<str:username>/', user_views.public_profile, name='public_profile'),

     path('edit-profile/<str:username>/', user_views.edit_profile, name='edit-profile'),
     path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
     path('password-reset-mobile/', auth_views.PasswordResetView.as_view(
          template_name='password_reset_mobile.html',
          success_url=reverse_lazy('password_reset_done_mobile')
     ), name='password_reset_mobile'),
     path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
     path('password-reset-mobile/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done_mobile.html'), name='password_reset_done_mobile'),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm_mobile.html'), name='password_reset_confirm'),
     path('password-reset-complete-mobile/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete_mobile.html'), name='password_reset_complete_mobile'),
     path('password-change-mobile/', auth_views.PasswordChangeView.as_view(template_name='password_change_mobile.html'), name='password_change_mobile'),
     path('password-change-mobile/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done_mobile.html'), name='password_change_done_mobile'),
     path('delete-account/', user_views.delete_account, name='delete-account'),
     path('deleted/', user_views.account_deleted, name='deleted'),
     path('logout/', user_views.logout_view, name='logout'),
     path('logout_mobile/', user_views.logout_view_mobile, name='logout_view_mobile'),
     path('contact/', user_views.contact_view, name='contact'),
     path('homepage/<str:username>/', user_views.home_logged_in, name='home_logged_in'),
     path('home/<str:username>/', user_views.home_logged_in_no_spotify, name='home_logged_in_no_spotify'),
     path('explore/', user_views.explore, name='explore'),
     path('i18n/', include('django.conf.urls.i18n')),
     path('wrap-generate/', user_views.wrap_generate, name='wrap_generate'),
     path('wrap-detail/<int:wrap_id>/', user_views.wrap_detail, name='wrap_detail'),
     path('wrap-detail-view/<int:wrap_id>/', user_views.wrap_detail_view, name='wrap_detail_view'),
     path('wrap-delete/<int:wrap_id>/', user_views.wrap_delete, name='wrap_delete'),
     path('delete-wrap/<int:wrap_id>/', user_views.wrap_delete, name='wrap_delete'),
     path('wrap-update-public/<int:wrap_id>/', user_views.wrap_update_public, name='wrap-update-public'),
     path('mobile_login/', user_views.login_view_mobile, name='login_mobile'),
     path('mobile_register/', user_views.register_mobile, name='register_mobile'),
     path('homepage_mobile/<str:username>/', user_views.home_logged_in_mobile, name='home_logged_in_mobile'),
     path('home-mobile/', user_views.home_mobile, name='home-mobile'),
]
