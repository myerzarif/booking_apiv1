"""Url Routes for Content App"""

from django.urls import path
from django.conf import settings
from .views import (
    HotelDetailView,
    DestinationView
)

app_name = 'content'

urlpatterns = [
    path('hotels/<str:code>', HotelDetailView.as_view(), name='hotel_detail'),
    path('destinations', DestinationView.as_view(), name='destinations_detail'),

]
