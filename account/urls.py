"""Url Routes for Account App"""

from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    UserDetailView,
    UserView
)

app_name = 'account'

urlpatterns = [
    path('user/login', LoginView.as_view(), name='login'),
    path('user/logout', LogoutView.as_view(), name='logout'),
    path('user/register', RegisterView.as_view(), name='register'),
    path('user/<str:pk>', UserDetailView.as_view(), name='user'),
    path('user', UserView.as_view(), name='user'),
]
