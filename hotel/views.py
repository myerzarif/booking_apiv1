from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import generics
from config.logger import LoggerMixin
from dataclasses import asdict
from .serializers import HotelAvailabilityQueryParamSerializer, HotelBookingQueryParamSerializer
from drf_yasg.utils import swagger_auto_schema
from .hotelbeds.availability import HbAvailability
from .hotelbeds.booking import HbBooking


class HotelAvailabilityView(LoggerMixin, generics.GenericAPIView):
    """
    Check Hotel Availability
    """
    permission_classes = []
    serializer_class = HotelAvailabilityQueryParamSerializer

    def post(self, request, *args, **kwargs):
        """
        Search Hotels
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        filters = serializer.validated_data
        availabilities = HbAvailability(filters=filters).remote_search()
        return Response(data=asdict(availabilities), status=200)

class HotelAvailabilityV2View(LoggerMixin, generics.GenericAPIView):
    """
    Check Hotel Availability V2
    """
    permission_classes = []
    serializer_class = HotelAvailabilityQueryParamSerializer

    def post(self, request, *args, **kwargs):
        """
        Search Hotels
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        filters = serializer.validated_data
        availabilities = HbAvailability(filters=filters).search_v2()
        return Response(data=availabilities, status=200)


class HotelBookingView(LoggerMixin, generics.GenericAPIView):
    """
    Hotel Booking
    """
    permission_classes = []
    serializer_class = HotelBookingQueryParamSerializer

    def post(self, request, *args, **kwargs):
        """
        Book Hotel
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        booking_response = HbBooking(params==params).book()
        return Response(data=asdict(booking_response), status=200)
