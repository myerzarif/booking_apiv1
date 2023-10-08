"""Url Routes for Car App"""

from django.urls import path
from django.conf import settings
from .views import (
    CarDetailView,
    CarView,
    CarUpdateAvailabilityView
)

app_name = 'car'

urlpatterns = [
    path('<str:code>', CarDetailView.as_view(), name='car_detail'),
    path('', CarView.as_view(), name='car_list_create'),
    path('update/availability', CarUpdateAvailabilityView.as_view(), name='car_update_availability'),
]
