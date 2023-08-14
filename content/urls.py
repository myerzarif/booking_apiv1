"""Url Routes for Content App"""

from django.urls import path
from django.conf import settings
from .views import (
    HotelDetailView
)

app_name = 'content'

urlpatterns = [
    path('hotels/<str:code>', HotelDetailView.as_view(), name='hotel_detail'),

]
