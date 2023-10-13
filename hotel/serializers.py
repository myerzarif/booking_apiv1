
from hotel.base.models import AvailabilityData
from rest_framework_dataclasses.serializers import DataclassSerializer
from rest_framework import serializers
from common.types import HOTEL_INFO_EXCLUDE_OPTIONS


class PaxDataSerializer(serializers.Serializer):
    type = serializers.ChoiceField(['AD', 'CH', 'IN', 'YD', 'SD'])
    age = serializers.IntegerField()


class OccupancyDataSerializer(serializers.Serializer):
    rooms = serializers.IntegerField()
    adults = serializers.IntegerField()
    children = serializers.IntegerField()
    paxes = PaxDataSerializer(many=True, required=False)


class StaySerializer(serializers.Serializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()


class HotelAvailabilityQueryParamSerializer(serializers.Serializer):
    stay = StaySerializer()
    destinations = serializers.ListField(
        child=serializers.CharField(), required=False)
    occupancies = OccupancyDataSerializer(many=True)
    hotels = serializers.ListField(
        child=serializers.CharField(), required=False)
    exclude = serializers.ListField(
        allow_null=True, child=serializers.ChoiceField(HOTEL_INFO_EXCLUDE_OPTIONS), required=False)


class HotelUpdateAvailabilityQueryParamSerializer(serializers.Serializer):
    stay = StaySerializer()
    occupancies = OccupancyDataSerializer(many=True)
    reservation_id = serializers.CharField()


class HotelOtherRoomAvailabilityQueryParamSerializer(serializers.Serializer):
    item_id = serializers.CharField()


class HotelAvailabilitySerializer(DataclassSerializer):
    """
    Serializer for Hotel Content View
    get a code and return the hotel data (some fields like [rooms, images, facilities] can be excluded in response)
    """

    class Meta:
        dataclass = AvailabilityData


class HolderSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


class HotelBookingQueryParamSerializer(serializers.Serializer):
    holder = HolderSerializer()
    rate_key = serializers.CharField(required=True)
    remark = serializers.CharField(required=False)
