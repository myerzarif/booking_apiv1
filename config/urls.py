"""
config URL Configuration
"""
from django.urls import path, include
from django.conf import settings
from account import urls as ACCOUNT_URL
from file import urls as FILE_URL
from content import urls as CONTENT_URL
from hotel import urls as HOTEL_URL
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
import os

schema_view = get_schema_view(
    openapi.Info(
        title="Booking - API V1",
        default_version='v1',
        description="Booking Platform",
    ),
    public=True,
    url=os.environ.get("BASE_URL_SWAGGER", "http://localhost/"),
    permission_classes=(AllowAny, )
)

urlpatterns = [
    path('api/v1/', include(ACCOUNT_URL)),
    path('api/v1/file/', include(FILE_URL)),
    path('api/v1/content/', include(CONTENT_URL)),
    path('api/v1/hotel/', include(HOTEL_URL)),
]

if settings.DEBUG or settings.ENVIRONMENT_APP != "PRODUCTION":
    urlpatterns.append(
        path('help', schema_view.with_ui('redoc', cache_timeout=0)))
    urlpatterns.append(
        path('help-swagger', schema_view.with_ui('swagger', cache_timeout=0)))
