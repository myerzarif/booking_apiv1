from django.utils import timezone
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework import generics, exceptions, permissions
from account.models import User
from .models import AccessToken, User
from .validators import confirm_password_validator
from .serializers import (
    AccessTokenSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer
)
from .authentication import get_user_agent_header
from config.logger import LoggerMixin
from django.contrib.auth.hashers import check_password
from common.pagination import MediumResultsSetPagination
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filter


class LoginView(LoggerMixin, generics.GenericAPIView):
    """
    Login with password
    """
    serializer_class = LoginSerializer
    permission_classes = []

    @method_decorator(ratelimit(key='post:email', method="POST", rate='6/m', block=True))
    def post(self, request):
        """Post Method View"""
        self.data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.get_user()
        if not check_password(serializer.validated_data["password"], user_obj.password):
            raise exceptions.ValidationError(
                detail="Incorrect Password!")

        origin = request.META.get('HTTP_ORIGIN')
        token = AccessToken.objects.create(user=user_obj, origin=origin or "",
                                           user_agent=get_user_agent_header(request))
        user_obj.last_login = timezone.now()
        user_obj.save()
        data = {
            "access_token": AccessTokenSerializer(instance=token,
                                                  context={'request': request}).data
        }
        return Response(data=data, status=200)


class RegisterView(LoggerMixin, generics.GenericAPIView):
    """
    Register User
    """
    serializer_class = RegisterSerializer
    permission_classes = []

    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='50/h', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='5/m', block=True))
    def post(self, request, *args, **kwargs):
        """Post Method View"""
        self.data = request.data
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirm_password_validator(request.data)
        self.perform_create(serializer)
        new_data = {**serializer.data}
        new_data.pop("password")
        return Response(new_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        obj = serializer.save()
        return obj


class UserDetailView(LoggerMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete User
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.parser_context['kwargs'].get('pk'))

    def destroy(self, request, *args, **kwargs):
        if request.user.role == User.UserRole.TECH:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(data={'detail': 'User deleted!'}, status=200)
        else:
            return Response(data={'detail': 'You don''t have access to delete user'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(LoggerMixin, generics.GenericAPIView):
    """
    Logout User and deactive Token
    """
    serializer_class = Serializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(data={"detail": "Logout Successfully!"}, status=200)


class UserView(LoggerMixin, generics.ListCreateAPIView):
    """
    List and Create User
    """
    serializer_class = UserSerializer
    pagination_class = MediumResultsSetPagination
    filter_backends = [filters.DjangoFilterBackend, rest_filter.SearchFilter]
    search_fields = ["email"]
    permission_classes = [permissions.IsAuthenticated]
    name = "user"

    def get_queryset(self):
        return User.objects.all().filter(active=True)
