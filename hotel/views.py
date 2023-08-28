from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import generics
from config.logger import LoggerMixin
from .hotelbeds.hotels import HbHotels
from dataclasses import asdict
from .serializers import HotelAvailabilitySerializer, HotelAvailabilityQueryParamSerializer
from drf_yasg.utils import swagger_auto_schema


class HotelAvailabilityView(LoggerMixin, generics.GenericAPIView):
    """
    Check Hotel Availability
    """
    permission_classes = []
    serializer_class = HotelAvailabilitySerializer

    @swagger_auto_schema(query_serializer=HotelAvailabilityQueryParamSerializer)
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='50/h', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='5/m', block=True))
    def get(self, request, *args, **kwargs):
        """
        Get Hotel Info
        """
        hotel = HbHotels().get_by_code(kwargs.get("code"),
                                       request.query_params.get("exclude", []))
        # HotelContentSerializer(instance=hotel).data
        return Response(data=asdict(hotel), status=200)
