
from django_restql.mixins import DynamicFieldsMixin
from content.base.models import HotelData, DestinationListData, StaticCountryListData
from rest_framework_dataclasses.serializers import DataclassSerializer
from rest_framework import serializers
from typing import Literal, Optional
from common.types import HOTEL_INFO_EXCLUDE_OPTIONS


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