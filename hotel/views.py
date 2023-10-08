from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import generics
from config.logger import LoggerMixin
from dataclasses import asdict
from .serializers import HotelAvailabilityQueryParamSerializer, HotelBookingQueryParamSerializer, HotelUpdateAvailabilityQueryParamSerializer
from drf_yasg.utils import swagger_auto_schema
from .hotelbeds.availability import HbAvailability
from .hotelbeds.booking import HbBooking
from transaction.models import Reservation
from rest_framework import exceptions


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


class HotelUpdateAvailabilityView(LoggerMixin, generics.GenericAPIView):
    """
    Check Hotel Availability Update
    """
    permission_classes = []
    serializer_class = HotelUpdateAvailabilityQueryParamSerializer

    def post(self, request, *args, **kwargs):
        """
        Search Hotels
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        filters = serializer.validated_data
        reservation = Reservation.objects.get(pk=filters.get("reservation_id"))
        if not reservation:
            raise exceptions.ValidationError(
                "Reservation is not valid! Please try to search again.")

        filters["hotels"] = [reservation.hotel_code]
        reservation_response = HbAvailability(
            filters=filters).hotel_update_search(reservation)
        return Response(data=reservation_response, status=200)


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
        booking_response = HbBooking(params == params).book()
        return Response(data=asdict(booking_response), status=200)
