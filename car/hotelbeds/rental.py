from car.base.rental import Rental
from car.hotelbeds.config import Config
from common.types import HttpMethods
from common.utils import generate_random_string
from cache_memoize import cache_memoize
from car.base.models import CarData
from common.extensions import mongo_default_db
from dataclasses import asdict
from common.decorators import check_null
from common.utils import to_decimal
from django.conf import settings
from rest_framework import exceptions


class HbRental(Rental):

    def __init__(self, params={}):
        self.config = Config(
            endpoint="/hotel-api/1.0/bookingstest",
            params=self.create_request_data(params),
            json=None,
            data=None,
            method=HttpMethods.POST
        )
        self.collection_name = "rental_car"

    def create_request_data(self, params):
        if not params:
            return None

        params = {
            "name": params.get("name", ""),
            "type": params.get("type", "")
        }

        return params

    @check_null()
    def get_dataclass_by_doc(self, doc):
        return CarData(
            code=doc.get("code"),
            name=doc.get("name"),
            description=doc.get("description"),
            type=doc.get("type"),
            image=doc.get("image"),
            active=doc.get("active"),
            price=to_decimal(doc.get("price"))
        )

    def search(self):
        return [asdict(self.get_dataclass_by_doc(item)) for item in list(mongo_default_db[self.collection_name].find(self.config.params).sort("price"))]

    def car_update_reservation(self, car, reservation_info):        
        days = reservation_info.search.get("days")
        hotel_amount = to_decimal(reservation_info.hotel_amount)
        hotel_fee_amount = to_decimal(reservation_info.hotel_fee_amount)
        total_hotel_amount = to_decimal(hotel_amount + hotel_fee_amount)

        car_amount = to_decimal(car.get("price", 0))
        car_fee_amount = to_decimal(
            car.get("price", 0) * settings.CAR_FEE_PERCENTAGE/100)
        total_car_amount = to_decimal(days * (car_amount + car_fee_amount))

        total_amount = to_decimal(
            hotel_amount + hotel_fee_amount + (days * (car_amount + car_fee_amount)))

        reservation_doc = {
            "car_code": car.get("code"),
            "car_name": car.get("name"),
            "total_amount": total_amount,
            "total_hotel_amount": total_hotel_amount,
            "total_car_amount": total_car_amount,
            "hotel_amount": hotel_amount,
            "car_amount": car_amount,
            "hotel_fee_amount": hotel_fee_amount,
            "car_fee_amount": car_fee_amount
        }

        result = reservation_info.update(reservation_doc)

        return result.to_dict()

    def car_update_search(self, data, reservation_info):
        car = self.get_doc_by_code(data.get("car_code", "")) or {}
        return self.car_update_reservation(car, reservation_info)
