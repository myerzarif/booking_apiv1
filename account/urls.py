"""Url Routes for Account App"""

from django.urls import path
from django.conf import settings
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    UserDetailView,
    UserView,
    ChangePasswordView,
    SendResetPasswordTokenView,
    ResetPasswordView,
    EmailVerificationView,
    UserInfoView,
    GetPasswordTokenView,
    OtpLoginView,
    OtpVerifyView,
    OtpResendView,
    GoogleLoginView,
    DashboardView
)

app_name = 'account'

urlpatterns = [
    path('user/login', LoginView.as_view(), name='login'),
    path('user/logout', LogoutView.as_view(), name='logout'),
    path('user/register', RegisterView.as_view(), name='register'),
    path('user/get_info', UserInfoView.as_view(), name='user_info'),
    path('user/<str:pk>', UserDetailView.as_view(), name='user'),
    path('user', UserView.as_view(), name='user'),
    path('user/password/change', ChangePasswordView.as_view(),
         name='change_password'),
    path('user/password/send_token', SendResetPasswordTokenView.as_view(),
         name='send_reset_password_token'),
    path('user/password/reset', ResetPasswordView.as_view(), name='reset_password'),
    path('user/verify_email', EmailVerificationView.as_view(), name='verify_email'),
    path('user/otp/login', OtpLoginView.as_view(), name='otp_login'),
    path('user/otp/verify', OtpVerifyView.as_view(), name='otp_verify'),
    path('user/otp/resend', OtpResendView.as_view(), name='otp_resend'),
    path('user/google/login', GoogleLoginView.as_view(), name='google_login'),
    path('dashboard', DashboardView.as_view(), name='dashboard_info'),
]

if settings.ENVIRONMENT_APP == 'DEVELOPE':
    urlpatterns.append(path('user/password/get_token',
                       GetPasswordTokenView.as_view(), name='get_password_token'))
