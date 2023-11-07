from django.utils import timezone
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework import generics, exceptions, permissions
from account.models import User
from .filters import UserFilter
from .models import AccessToken, User
from .validators import confirm_password_validator
import requests

from .serializers import (
    AccessTokenSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    EmailVerificationSerializer,
    OtpLoginSerializer,
    OtpVerifySerializer,
    GoogleLoginSerializer,
    DashboardSerializer
)
from .authentication import get_user_agent_header
from config.logger import LoggerMixin
from django.contrib.auth.hashers import check_password, make_password
from common.pagination import MediumResultsSetPagination
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filter
from django.conf import settings


class LoginView(LoggerMixin, generics.GenericAPIView):
    """
    Login with password
    """
    serializer_class = LoginSerializer
    permission_classes = []

    @method_decorator(ratelimit(key='post:username', method="POST", rate='20/m', block=True))
    def post(self, request):
        """Post Method View"""
        self.data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.get_user()
        if not check_password(serializer.validated_data["password"], user_obj.password):
            raise exceptions.ValidationError("Incorrect Password!")
        origin = request.META.get('HTTP_ORIGIN')
        token = AccessToken.objects.create(user=user_obj, origin=origin or "",
                                           user_agent=get_user_agent_header(request))
        user_obj.last_login = timezone.now()
        user_obj.save()
        data = AccessTokenSerializer(instance=token, context={
                                     'request': request}).data
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


class UserInfoView(LoggerMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Serializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data, status=200)


class UserView(LoggerMixin, generics.ListCreateAPIView):
    """
    List and Create User
    """
    serializer_class = UserSerializer
    pagination_class = MediumResultsSetPagination
    filter_backends = [filters.DjangoFilterBackend, rest_filter.SearchFilter]
    filterset_class = UserFilter
    search_fields = ('email', 'first_name', 'last_name', 'mobile', 'role')
    permission_classes = [permissions.IsAuthenticated]
    name = "user"

    def get_queryset(self):
        return User.objects.filter(active=True)


class ChangePasswordView(LoggerMixin, generics.GenericAPIView):
    """
    Change Password for a Logged in User
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        self.data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validate_user(request.user.email)
        origin = request.META.get('HTTP_ORIGIN')
        request.auth.delete()
        token = AccessToken.objects.create(user=user_obj, origin=origin or "",
                                           user_agent=get_user_agent_header(request))
        user_obj.password = make_password(
            serializer.validated_data["new_password"])
        user_obj.last_login = timezone.now()
        user_obj.save()
        data = AccessTokenSerializer(instance=token, context={
                                     'request': request}).data
        return Response(data=data, status=200)


class SendResetPasswordTokenView(LoggerMixin, generics.GenericAPIView):
    """
    Generate a reset password token and send it via email
    """
    serializer_class = ForgotPasswordSerializer
    permission_classes = []

    def post(self, request):
        self.data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_password_reset_url()
        return Response(data={"detail": "Password reset email will be sent!"}, status=201)


class ResetPasswordView(LoggerMixin, generics.GenericAPIView):
    """
    Reset the forgotten password based on user_id and token
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request):
        self.data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.get_user()

        # ? IS IT OK TO LOG USER IN WITH NEW PASSWORD?
        origin = request.META.get('HTTP_ORIGIN')
        token = AccessToken.objects.create(user=user_obj, origin=origin or "",
                                           user_agent=get_user_agent_header(request))
        user_obj.password = make_password(
            serializer.validated_data["new_password"])
        user_obj.last_login = timezone.now()
        user_obj.save()
        data = {'detail': 'Reset Password Done!'}
        return Response(data=data, status=200)


class EmailVerificationView(LoggerMixin, generics.GenericAPIView):
    """
    verify email based on user_id and token
    """
    serializer_class = EmailVerificationSerializer
    permission_classes = []

    def post(self, request):
        self.data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.verify_token()

        # ? IS IT OK TO LOG USER IN WITH NEW PASSWORD?
        user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()
        data = {'detail': 'email is verified!'}
        return Response(data=data, status=200)


class GetPasswordTokenView(LoggerMixin, generics.GenericAPIView):
    """
    Generate a reset password token and return
    """
    serializer_class = ForgotPasswordSerializer
    permission_classes = []

    def post(self, request):
        self.data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if settings.ENVIRONMENT_APP != 'DEVELOPE':
            raise exceptions.ValidationError("Only for test purposes!")
        data = serializer.get_password_reset_token_object()
        return Response(data={'token': data['token'], 'user_id': data['user_id'], }, status=200)


class OtpLoginView(LoggerMixin, generics.GenericAPIView):
    """
    OTP Login 
    """
    serializer_class = OtpLoginSerializer
    permission_classes = []

    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='2/s', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='20/m', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='50/h', block=True))
    @method_decorator(ratelimit(key='post:username', method="POST", rate='2/m', block=True))
    @method_decorator(ratelimit(key='post:username', method="POST", rate='8/h', block=True))
    @method_decorator(ratelimit(key='post:username', method="POST", rate='20/d', block=True))
    def post(self, request):
        """Post Method View"""
        self.data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.send_otp()

        data = {'detail': 'OTP sent successfully!', 'token': token}

        return Response(data=data, status=status.HTTP_201_CREATED)


class OtpVerifyView(LoggerMixin, generics.GenericAPIView):
    """
    OTP Verify 
    """
    serializer_class = OtpVerifySerializer
    permission_classes = []

    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='2/s', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='20/m', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='50/h', block=True))
    def post(self, request):
        """Post Method View"""
        self.data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.token_validate()
        origin = request.META.get('HTTP_ORIGIN')
        token = AccessToken.objects.create(user=user_obj, origin=origin or "",
                                           user_agent=get_user_agent_header(request))
        user_obj.last_login = timezone.now()
        user_obj.save()
        data = AccessTokenSerializer(instance=token, context={
                                     'request': request}).data
        return Response(data=data, status=200)


class OtpResendView(LoggerMixin, generics.GenericAPIView):
    """
    OTP Resend 
    """
    serializer_class = OtpLoginSerializer
    permission_classes = []

    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='2/s', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='20/m', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='50/h', block=True))
    @method_decorator(ratelimit(key='post:username', method="POST", rate='2/m', block=True))
    @method_decorator(ratelimit(key='post:username', method="POST", rate='8/h', block=True))
    @method_decorator(ratelimit(key='post:username', method="POST", rate='20/d', block=True))
    def post(self, request):
        """Post Method View"""
        self.data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.resend_otp()

        data = {'detail': 'OTP sent successfully!', 'token': token}

        return Response(data=data, status=status.HTTP_201_CREATED)


class GoogleLoginView(LoggerMixin, generics.GenericAPIView):
    """
    Generate Token and validate id_token google
    parameters of login is id_token google
    return access token consist: Key, User
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = GoogleLoginSerializer

    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='20/m', block=True))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_token = serializer.validated_data["id_token"]
        email = self.validate_token_google(id_token)
        user = self.get_user_by_mail(email)
        origin = request.META.get('HTTP_ORIGIN')
        token = AccessToken.objects.create(user=user, origin=origin or "",
                                           user_agent=get_user_agent_header(request))
        user.last_login = timezone.now()
        user.save()
        data = AccessTokenSerializer(instance=token, context={'request': request}).data
        return Response(data=data, status=200)

    def get_user_by_mail(self, email):
        users = User.objects.filter(email=email)
        if users:
            user_obj = users[0]
            user_obj.email_verified = True
            user_obj.status = User.UserStatus.ACTIVE
            user_obj.save()
        else:
            user_obj = User()
            user_obj.email = email
            user_obj.email_verified = True
            user_obj.status = User.UserStatus.ACTIVE
        return user_obj


    def validate_token_google(self, id_token):
        try:
            response = requests.get(
                settings.GOOGLE_ID_TOKEN_INFO_URL,
                params={'id_token': id_token}
            )
            if not response.ok:
                raise exceptions.ValidationError("Google Authentication Failed!")

            audience = response.json()['aud']

            if audience != settings.GOOGLE_OAUTH2_CLIENT_ID:
                raise exceptions.ValidationError("Google Authentication Failed!")

            return response.json()["email"]
        except Exception as e:
            raise exceptions.ValidationError("Google Authentication Failed!")


class DashboardView(LoggerMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DashboardSerializer

    def get(self, request):
        serializer = self.get_serializer()
        data = serializer.get_info()
        return Response(data=data, status=200)
