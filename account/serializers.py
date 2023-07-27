"""
define Serialize instance to json format
also define validator for input data
"""

from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from rest_framework import exceptions
from django_restql.mixins import DynamicFieldsMixin
from .models import AccessToken, User
from .validators import email_validator, password_validator, address_validator
from django.contrib.auth.hashers import make_password


class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """Serializer For User Model"""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "created_at",
            "last_login",
        ]
        read_only_fields = ['id']


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
    get email and password
    """
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def get_user(self):
        validated_data = self.validated_data
        try:
            return User.objects.get(email=validated_data["email"])
        except User.DoesNotExist:
            raise exceptions.NotFound("The user does not exist!")
