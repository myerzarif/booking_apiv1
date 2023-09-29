"""
define Serialize instance to json format
also define validator for input data
"""

from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from rest_framework import exceptions
from django_restql.mixins import DynamicFieldsMixin
from .models import AccessToken, User
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from common.tasks import send_email_celery, send_sms_celery
from django.contrib.auth.hashers import make_password
from common.utils import generate_strong_password, random_otp_generator
from common.tasks import send_email_celery
from django.conf import settings
from datetime import datetime
from django.utils.http import base36_to_int, int_to_base36
from django.utils.crypto import constant_time_compare, salted_hmac
from common.types import UserType
from django.core.cache import cache
from config.settings import REDIS_HOST, REDIS_PORT
import redis
import random
import logging
from .validators import (
    email_validator,
    password_validator,
    validate_email,
    validate_confirm,
    username_type,
)

logger = logging.getLogger('project.account')


class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """Serializer For User Model"""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "mobile",
            "job_title",
            "created_at",
            "last_login",
            "role",
            "status",
        ]
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        logged_in_user = None
        request = self.context.get('request', None)
        if request:
            logged_in_user = request.user

        if "status" in validated_data:
            # only tech and admin can change the status of a user
            if logged_in_user.role in [User.UserRole.TECH, User.UserRole.ADMIN]:
                setattr(instance, "status", validated_data["status"])
            else:
                raise exceptions.PermissionDenied()
        if "email" in validated_data:
            # only tech can change email
            if logged_in_user.role == User.UserRole.TECH:
                setattr(instance, "email", validated_data["email"])
            else:
                raise exceptions.PermissionDenied()
        if "role" in validated_data:
            # only user with higher role can change role of other users
            if logged_in_user.role == User.UserRole.TECH or \
                    (logged_in_user.role == User.UserRole.ADMIN and instance.role != User.UserRole.TECH):
                # prevent user to downgrade or change his role
                if logged_in_user.id != instance.id:
                    setattr(instance, "role", validated_data["role"])
            else:
                raise exceptions.PermissionDenied()

        for attr, value in validated_data.items():
            if attr in ["first_name", "last_name", "mobile", "job_title"]:
                setattr(instance, attr, value)

        instance.save()
        return instance

    def create(self, validated_data):
        request = self.context.get('request', None)

        if request.user.role not in [User.UserRole.TECH, User.UserRole.ADMIN]:
            raise exceptions.PermissionDenied()

        password = generate_strong_password()
        send_email_celery(
            subject="New User",
            to=validated_data["email"],
            title="Dear {0}".format(validated_data["email"]),
            start_lines=['Please find below credentials regarding to your account in Booking Platform',
                         'Username: {}'.format(validated_data["email"]), 'Password: {}'.format(password)],
            links=[
                {'url': settings.FRONT_BASE_URL, 'text': 'Backoffice URL'}
            ],
            cc=''
        )

        validated_data["password"] = make_password(password)
        validated_data["status"] = User.UserStatus.ACTIVE
        return super().create(validated_data)


class AccessTokenSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """Serializer for AccessToken Model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = AccessToken
        fields = ["user", "key", "created", "expire_time", "is_active",
                  "user_agent", "origin"]


class RegisterSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """Serializer for User Model for Registration"""
    email = serializers.CharField(
        max_length=200,
        validators=[
            email_validator,
            UniqueValidator(queryset=User.objects.all())
        ])

    password = serializers.CharField(
        max_length=200,
        validators=[
            password_validator
        ])

    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class LoginSerializer(DynamicFieldsMixin, serializers.Serializer):
    """
    Serializer for Login View
    get username and password 
    for now username can be only email
    in future we can develop login with phone too
    """
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def get_user(self):
        validated_data = self.validated_data
        try:
            user = User.objects.get(email=validated_data["username"])
            if user.status != User.UserStatus.ACTIVE:
                raise exceptions.ValidationError("User is not active!")
            return user
        except User.DoesNotExist:
            raise exceptions.NotFound("The user does not exist!")


class ChangePasswordSerializer(DynamicFieldsMixin, serializers.Serializer):
    """
    Serializer for Change Password View
    get email, old password, new password and password 
    """

    email = serializers.CharField(required=False)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=False)

    def validate_user(self, loggedUser):
        validated_data = self.validated_data

        if not validated_data.get("email"):
            validated_data["email"] = loggedUser

        validate_email(loggedUser, validated_data["email"])
        validate_confirm(
            validated_data["new_password"], validated_data.get("confirm_password"))
        password_validator(validated_data["new_password"])

        try:
            user = User.objects.get(email=validated_data["email"])
            if not user.check_password(validated_data["old_password"]):
                raise exceptions.ValidationError("Old password is incorrect!")
            return user
        except User.DoesNotExist:
            raise exceptions.NotFound("The user does not exist!")


class ForgotPasswordSerializer(DynamicFieldsMixin, serializers.Serializer):
    """
    Serializer for Forgot Password View
    """

    username = serializers.CharField(required=True)

    def get_password_reset_token_object(self):
        validated_data = self.validated_data
        username = validated_data["username"]
        usernameType = username_type(username)
        user = None
        try:
            if usernameType == UserType.email:
                user = User.objects.get(email=username)
            elif usernameType == UserType.mobile:
                user = User.objects.get(mobile=username)
            elif usernameType == UserType.uuid:
                user = User.objects.get(id=username)
        except User.DoesNotExist:
            raise exceptions.NotFound("The user does not exist!")

        return {
            'token': PasswordResetTokenGenerator().make_token(user),
            'user_id': user.id,
            'user': user,
            'username_type': usernameType,
            'username': username,
        }

    def send_password_reset_url(self):
        token_object = self.get_password_reset_token_object()

        reset_password_url = '{0}/{1}/{2}/{3}'.format(
            settings.FRONT_BASE_URL,
            settings.RESET_PASSWORD_URL,
            token_object['user_id'],
            token_object['token'],
        )
        try:
            if token_object['username_type'] == UserType.email:
                send_email_celery(
                    subject="Reset Password",
                    to=token_object["username"],
                    title="Dear {0}".format(token_object["username"]),
                    start_lines=['Please click on below link and select a new password.',
                                 'Don''t share this link with anyone.', ''],
                    links=[
                        {'url': reset_password_url, 'text': 'Reset password URL'}
                    ],
                    cc=''
                )
            elif token_object['username_type'] == UserType.mobile:
                send_sms_celery(
                    msisdn=token_object["username"],
                    body='Please click on below link and select a new password.\nDon''t share this link with anyone.\n{0}'.format(
                        reset_password_url),
                )
        except Exception as e:
            raise Exception("Something went wrong: {0}".format(str(e)))


class ResetPasswordSerializer(DynamicFieldsMixin, serializers.Serializer):
    """
    Serializer for Reset Password View
    """

    # email = serializers.CharField(required=True)
    user_id = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def get_user(self):
        validated_data = self.validated_data
        validate_confirm(
            validated_data["new_password"], validated_data.get("confirm_password"))
        password_validator(validated_data["new_password"])
        user = None
        # username = force_text(urlsafe_base64_decode(validated_data["username_base64"]))
        user_id = validated_data["user_id"]
        token = validated_data["token"]
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.NotFound("The user does not exist!")

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise exceptions.ValidationError(
                "The URL is expired or is incorrect!")
        return user


class EmailVerificationSerializer(DynamicFieldsMixin, serializers.Serializer):
    """
    Serializer for Email Verification View
    """

    user_id = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def verify_token(self):
        validated_data = self.validated_data
        user = None
        user_id = validated_data["user_id"]
        token = validated_data["token"]
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.NotFound("The user does not exist!")

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise exceptions.ValidationError(
                "The URL is expired or is incorrect!")
        return user


class OtpLoginSerializer(DynamicFieldsMixin, serializers.Serializer):
    """
    Serializer for Otp Login View
    get email or phone number
    """
    username = serializers.CharField(write_only=True)

    def generate_token(self, username):
        dt = datetime.now()
        timestamp = int((dt - datetime(2001, 1, 1)).total_seconds())
        ts_b36 = int_to_base36(timestamp)
        hash_string = salted_hmac(
            key_salt="django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash",
            value=username + str(timestamp),
            algorithm='sha1',
        ).hexdigest()
        return "%s-%s" % (ts_b36, hash_string)

    def send_otp(self):
        validated_data = self.validated_data
        username = validated_data["username"]
        user_type = username_type(username)

        if user_type not in [UserType.mobile, UserType.email]:
            raise exceptions.ValidationError('username type is not valid!')

        otp_str = random_otp_generator()
        message_text = "This is your OTP on Alkhadra. Please don't share with anyone else."
        if user_type == UserType.email:
            send_email_celery(
                subject="One Time Password",
                to=username,
                title="Dear {0}".format(username),
                start_lines=[message_text, 'OTP: {0}'.format(otp_str), ''],
                links=[],
                cc=''
            )
        elif user_type == UserType.mobile:
            send_sms_celery(
                msisdn=username,
                body='{0}\nOTP: {1}'.format(message_text, otp_str),
            )
        token = self.generate_token(username)
        cache.set(f"otp_{username}", otp_str, 120)
        cache.set(f"otp_token_{token}", username, 120)
        return token

    def resend_otp(self):
        validated_data = self.validated_data
        username = validated_data["username"]
        user_type = username_type(username)

        if user_type not in ["email", "phone"]:
            raise exceptions.ValidationError('username type is not valid!')

        r = redis.StrictRedis(
            host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        if not r.exists("otp_"+username):
            return self.send_otp()
        # otp sent before
        remain_seconds = r.ttl("otp_"+username)
        if remain_seconds < 10:
            # remove token and otp from redis
            r.persist("otp_" + username)
            return self.send_otp()
        else:
            raise exceptions.ValidationError(
                'Please wait for a few seconds to send a new otp!')


class OtpVerifySerializer(DynamicFieldsMixin, serializers.Serializer):
    token = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    def get_username_and_otp(self):
        username = cache.get(f"otp_token_{self.token}") or None
        otp = cache.get(f"otp_{username}") or None
        return username, otp

    def otp_validate(self):
        if settings.ENVIRONMENT_APP is not 'PRODUCTION' and self.otp == '11111':
            return

        if self.otp == self.request_otp:
            return

        attempts = cache.get(f"otp_attempt_{self.otp}{self.username}") or "1"
        if attempts == "3":
            raise exceptions.NotAcceptable(
                "Maximum wrong attempts are exceeded, please try later!")

        cache.set(f"otp_attempt_{self.otp}{self.username}", str(
            int(attempts)+1), 120)
        raise exceptions.NotAcceptable("The otp is not correct")

    def token_validate(self):
        validated_data = self.validated_data
        self.token = validated_data['token']
        self.request_otp = validated_data['otp']
        self.username, self.otp = self.get_username_and_otp()
        self.otp_validate()

        if not self.username:
            raise exceptions.NotAcceptable(
                "The token is expired! or the token is not valid")
        if not self.otp:
            raise exceptions.NotAcceptable(
                "The otp is expired! please try again.")

        user_type = username_type(self.username)

        if user_type == UserType.email:
            users = User.objects.filter(email=self.username)
            if users:
                u = users[0]
                u.email_verified = True
                u.save()
                return u
        elif user_type == UserType.mobile:
            users = User.objects.filter(mobile=self.username)
            if users:
                u = users[0]
                u.mobile_verified = True
                u.save()
                return u

        # create user if needed and return it
        user = User()
        if user_type == UserType.email:
            user.email = self.username
            user.email_verified = True
            user.status = User.UserStatus.ACTIVE
        else:
            user.mobile = self.username
            user.mobile_verified = True
            user.status = User.UserStatus.ACTIVE
        try:
            user.save()
            return user
        except Exception as e:
            raise exceptions.NotAcceptable(
                "Can not save new user: {0}".format(str(e)))
