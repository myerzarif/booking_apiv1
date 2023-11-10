from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import generics
from config.logger import LoggerMixin
from .hotelbeds.hotels import HbHotels, HbDestinations
from .base.locations import StaticCountries
from dataclasses import asdict
from .serializers import HotelContentSerializer, HotelContentQueryParamSerializer, DestinationSerializer, StaticCountrySerializer, HotelQueryParamSerializer, HotelListSerializer
from drf_yasg.utils import swagger_auto_schema


class HotelDetailView(LoggerMixin, generics.GenericAPIView):
    """
    Find Hotel
    """
    permission_classes = []
    lookup_field = 'code'
    serializer_class = HotelContentSerializer

    @swagger_auto_schema(query_serializer=HotelContentQueryParamSerializer)
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='50/h', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='5/m', block=True))
    def get(self, request, *args, **kwargs):
        """
        Get Hotel Info
        """
        hotel = HbHotels().get_by_code(kwargs.get("code"),
                                       request.query_params.get("exclude", []))
        # HotelContentSerializer(instance=hotel).data
        return Response(data=asdict(hotel), status=200)


class DestinationView(LoggerMixin, generics.GenericAPIView):
    """
    Available Destinations
    """
    permission_classes = []
    serializer_class = DestinationSerializer

    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='60/h', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='10/m', block=True))
    def get(self, request, *args, **kwargs):
        """
        Get Available Destinations
        """
        destinations = HbDestinations().get_available_destinations()
        return Response(data=destinations, status=200)


class StaticCountriesView(LoggerMixin, generics.GenericAPIView):
    """
    Static Countries
    """
    permission_classes = []
    serializer_class = StaticCountrySerializer

    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='100/h', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='15/m', block=True))
    def get(self, request, *args, **kwargs):
        """
        Get Static Countries
        """
        countries = StaticCountries().get_static_countries()
        return Response(data=countries, status=200)


class HotelContentView(LoggerMixin, generics.GenericAPIView):
    """
    Hotel Lists
    """
    permission_classes = []
    serializer_class = HotelListSerializer

    @swagger_auto_schema(query_serializer=HotelQueryParamSerializer)
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='60/h', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='20/m', block=True))
    def get(self, request, *args, **kwargs):
        """
        Get Hotel Info
        """

        hotels = HbHotels().search(params=request.query_params.dict())
        return Response(data=hotels, status=200)
