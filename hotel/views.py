from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import generics
from config.logger import LoggerMixin
from dataclasses import asdict
from .serializers import HotelAvailabilitySerializer, HotelAvailabilityQueryParamSerializer
from drf_yasg.utils import swagger_auto_schema
from .hotelbeds.availability import HbAvailability


# class HotelAvailabilityView(LoggerMixin, generics.GenericAPIView):
#     """
#     Check Hotel Availability
#     """
#     permission_classes = []
#     serializer_class = HotelAvailabilityQueryParamSerializer

#     @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='50/h', block=True))
#     @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='5/m', block=True))
#     def post(self, request, *args, **kwargs):
#         """
#         Search Hotels
#         """
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         query_data = serializer.validated_data
#         print("query_data", query_data)

#         return Response(data={}, status=200)


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
        # availabilities = HbAvailability(filters=request.data).search()
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.search()
        # serializer.is_valid(raise_exception=True)
        # print("serializer", serializer)
        # print("dir", dir(serializer))
        # print("validated_data", serializer.data)

        # print("request data", request.data)
        # serializer.is_valid(raise_exception=True)
        # hotel = HbAvailability(filters=kwargs)
        # HotelContentSerializer(instance=hotel).data
        # return Response(data=asdict(availabilities), status=200)
