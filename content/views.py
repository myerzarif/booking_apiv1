from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import generics
from config.logger import LoggerMixin
from .hotelbeds.hotels import HbHotels
from content.general.hotels import Hotels
from content.general.locations import Countries
from dataclasses import asdict


class HotelDetailView(LoggerMixin, generics.GenericAPIView):
    """
    Find Hotel
    """
    permission_classes = []
    lookup_field = 'code'

    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='50/h', block=True))
    @method_decorator(ratelimit(key='header:x-forwarded-for', method="POST", rate='5/m', block=True))
    def get(self, request, *args, **kwargs):
        """Post Method View"""
        hotel = HbHotels().get_by_code(kwargs.get("code"))
        # country = Countries.CountryData("AD", "Andorra", "CA", "CANILLO")
        # hotel = Hotels.HotelData("1234", "hotel name", "in dubai", country)

        # print("find_hotel_by_code", hb.find_hotel_by_code(kwargs.get("code")))
        return Response(data=asdict(hotel), status=200)
