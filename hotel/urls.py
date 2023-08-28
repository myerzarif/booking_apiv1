"""Url Routes for Content App"""

from django.urls import path
from django.conf import settings
from .views import (
    HotelAvailabilityView
)

app_name = 'hotel'

urlpatterns = [
    path('availability', HotelAvailabilityView.as_view(),
         name='hotel_availability'),

]
