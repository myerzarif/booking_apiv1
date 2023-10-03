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
        cars = [asdict(self.get_dataclass_by_doc(item)) for item in list(mongo_default_db[self.collection_name].find(self.config.params).sort("price"))]
        return cars