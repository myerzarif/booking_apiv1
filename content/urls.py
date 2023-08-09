"""Url Routes for Content App"""

from django.urls import path
from django.conf import settings
from .views import (
    AdhocUpdate
)

app_name = 'content'

urlpatterns = [
    path('adhoc_update', AdhocUpdate.as_view(), name='adhoc_update'),
]
