from django.utils import timezone
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework import generics, exceptions, permissions
from account.models import User
from config.logger import LoggerMixin
from django.contrib.auth.hashers import check_password, make_password
from common.pagination import MediumResultsSetPagination
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filter
from django.conf import settings
from .hotelbeds.commands import initial_type_insert

class InitialStaticFilesInsert(LoggerMixin, generics.GenericAPIView):
    """
    Login with password
    """
    permission_classes = []

    @method_decorator(ratelimit(key='post:username', method="POST", rate='20/m', block=True))
    def post(self, request):
        """Post Method View"""
        return Response(data={"detail": "Successfully Inserted!"}, status=200)
