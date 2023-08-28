
from django_restql.mixins import DynamicFieldsMixin
from hotel.base.models import AvailabilityData
from rest_framework_dataclasses.serializers import DataclassSerializer
from rest_framework import serializers
from typing import Literal, Optional


class HotelAvailabilitySerializer(DataclassSerializer):
    """
    Serializer for Hotel Content View
    get a code and return the hotel data (some fields like [rooms, images, facilities] can be excluded in response)
    """

    class Meta:
        dataclass = HotelData


class HotelAvailabilityQueryParamSerializer(serializers.Serializer):
    exclude = serializers.ListField(allow_null=True, child=serializers.ChoiceField(
        ['rooms', 'images', 'facilities', 'interest_points']))
