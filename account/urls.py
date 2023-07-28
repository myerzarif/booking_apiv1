"""Url Routes for Account App"""

from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    UserDetailView,
    UserView,
    ChangePasswordView,
    SendResetPasswordTokenView,
    ResetPasswordView,
    EmailVerificationView
)

app_name = 'account'

urlpatterns = [
    path('user/login', LoginView.as_view(), name='login'),
    path('user/logout', LogoutView.as_view(), name='logout'),
    path('user/register', RegisterView.as_view(), name='register'),
    path('user/<str:pk>', UserDetailView.as_view(), name='user'),
    path('user', UserView.as_view(), name='user'),
    path('user/password/change', ChangePasswordView.as_view(), name='change_password'),
    path('user/password/send_token', SendResetPasswordTokenView.as_view(), name='send_reset_password_token'),
    path('user/password/reset', ResetPasswordView.as_view(), name='reset_password'),
    path('user/verify_email', EmailVerificationView.as_view(), name='verify_email'),
]
