
from django_restql.mixins import DynamicFieldsMixin
from content.base.models import HotelData, DestinationListData, StaticCountryListData
from rest_framework_dataclasses.serializers import DataclassSerializer
from rest_framework import serializers
from typing import Literal, Optional
from common.types import HOTEL_INFO_EXCLUDE_OPTIONS
from account.models import User
from .hotelbeds.hotels import HbHotels
from rest_framework import exceptions 

class HotelContentSerializer(DataclassSerializer):
    """
    Serializer for Hotel Content View
    get a code and return the hotel data (some fields like [rooms, images, facilities] can be excluded in response)
    """

    class Meta:
        dataclass = HotelData


class HotelContentQueryParamSerializer(serializers.Serializer):
    exclude = serializers.ListField(
        allow_null=True, child=serializers.ChoiceField(HOTEL_INFO_EXCLUDE_OPTIONS))


class DestinationSerializer(DataclassSerializer):
    """
    Serializer for available Destinations
    """

    class Meta:
        dataclass = DestinationListData


class StaticCountrySerializer(DataclassSerializer):
    """
    Serializer for static Countries
    """

    class Meta:
        dataclass = StaticCountryListData


class HotelListSerializer(serializers.Serializer):
    """
    Serializer for Hotel Content View
    """

    name = serializers.CharField()
    code = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    active = serializers.BooleanField()


class HotelQueryParamSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    code = serializers.IntegerField(required=False)
    offset = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(required=False)


class HotelBlockSerializer(serializers.Serializer):
    active = serializers.BooleanField(required=True)
    code = serializers.CharField(required=True)

    def block(self, data):
        logged_in_user = None
        request = self.context.get('request', None)
        if request:
            logged_in_user = request.user

        if logged_in_user.role in [User.UserRole.TECH, User.UserRole.ADMIN]:
            HbHotels().block(data.get("code"), data.get("active"))
        else:
            raise exceptions.PermissionDenied()
