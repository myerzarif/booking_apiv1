"""Url Routes for Content App"""

from django.urls import path
from django.conf import settings
from .views import (
    InitialStaticFilesInsert
)

app_name = 'content'

urlpatterns = [
    path('initial_static_files_insert', InitialStaticFilesInsert.as_view(), name='adhoc_update'),
]
