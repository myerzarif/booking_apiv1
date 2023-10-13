"""Url Routes for Content App"""

from django.urls import path
from django.conf import settings
from .views import (
    HotelAvailabilityView,
    HotelAvailabilityV2View,
    HotelUpdateAvailabilityView,
    HotelOtherRoomAvailabilityView
)

app_name = 'hotel'

urlpatterns = [
    path('availability', HotelAvailabilityView.as_view(),
         name='hotel_availability'),
    path('v2/availability', HotelAvailabilityV2View.as_view(),
         name='hotel_availability_v2'),
    path('update/availability', HotelUpdateAvailabilityView.as_view(),
         name='hotel_update_availability'),
    path('rooms/availability', HotelOtherRoomAvailabilityView.as_view(),
         name='other_rooms'),
]
