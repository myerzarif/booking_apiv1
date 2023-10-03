from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import generics, permissions
from config.logger import LoggerMixin
from dataclasses import asdict
from .serializers import CarRentalSerializer, CarQueryParamSerializer, CarSerializer
from drf_yasg.utils import swagger_auto_schema
from .hotelbeds.rental import HbRental
from account.authentication import custom_permission_classes


class CarDetailView(LoggerMixin, generics.GenericAPIView):
    """
    Find Rental Car
    """
    permission_classes = []
    lookup_field = 'code'
    serializer_class = CarRentalSerializer

    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='50/h', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='5/m', block=True))
    def get(self, request, *args, **kwargs):
        """
        Get Hotel Info
        """
        car = HbRental().get_by_code(kwargs.get("code"))
        return Response(data=asdict(car), status=200)


class CarView(LoggerMixin, generics.GenericAPIView):
    """
    Search and Create Car
    """
    permission_classes = []
    serializer_class = CarSerializer

    @custom_permission_classes((permissions.IsAuthenticated,))
    def post(self, request, *args, **kwargs):
        """
        Create Car
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = serializer.create(serializer.validated_data)
        return Response(data=car, status=200)

    @swagger_auto_schema(query_serializer=CarQueryParamSerializer)
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='50/h', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="GET", rate='5/m', block=True))
    def get(self, request, *args, **kwargs):
        """
        Get Car Info
        """
        
        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # filters = serializer.validated_data
        print("request.query_params", request.query_params)
        print("dir(request.query_params)", dir(request.query_params))
        print("request.query_params.dict()", request.query_params.dict())
        
        cars = HbRental(params=request.query_params.dict()).search()
        return Response(data=cars, status=200)
