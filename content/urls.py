"""Url Routes for Content App"""

from django.urls import path
from django.conf import settings
from .views import (
    HotelDetailView,
    DestinationView,
    StaticCountriesView
)

app_name = 'content'

urlpatterns = [
    path('hotels/<str:code>', HotelDetailView.as_view(), name='hotel_detail'),
    path('destinations', DestinationView.as_view(), name='destinations_detail'),
    path('countries', StaticCountriesView.as_view(), name='countries_detail'),
]
