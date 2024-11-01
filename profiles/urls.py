from re import template
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from allauth.socialaccount import providers
from allauth import app_settings
from importlib import import_module

urlpatterns = [
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('sign-up/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name="logout"),
    path('profile/', views.update_profile, name="profile-page"),
    path('user-dashboard/', views.user_dashboard, name="user-dashboard"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="profiles/reset-password.html"), name='password_reset'), # gets users email
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="profiles/password-reset-done.html"), name='password_reset_done'), #tells user email has been sent
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="profiles/password_change.html"), name='password_reset_confirm'), # gives user form to enter new password
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="profiles/password_reset_complete.html"), name="password_reset_complete"),# tells user he can now sign in
    path('account_inactive/', views.account_inactive_all_auth_problem, name="account_inactive")
   ]
    # path('login/', auth_views.LoginView.as_view(template_name="profiles/login.html"), name="login"),
    # path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
 



if app_settings.SOCIALACCOUNT_ENABLED:
    urlpatterns += [path("social/", include("allauth.socialaccount.urls"))]

# Provider urlpatterns, as separate attribute (for reusability).
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns

