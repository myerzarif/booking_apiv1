from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import generics
from config.logger import LoggerMixin
from dataclasses import asdict
from .serializers import HotelAvailabilitySerializer, HotelAvailabilityQueryParamSerializer
from drf_yasg.utils import swagger_auto_schema
from .hotelbeds.availability import HbAvailability


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
        availabilities = HbAvailability(filters=filters).search()
        return Response(data=asdict(availabilities), status=200)
