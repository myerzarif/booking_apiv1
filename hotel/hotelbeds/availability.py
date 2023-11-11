from hotel.base.availability import Availability
from content.hotelbeds.config import Config
from hotel.base.models import (AvailabilityData,
                               AvailableHotelData,
                               AvailableRoomData,
                               RateData,
                               CancellationPlicyData,
                               AvailabilityTaxData,
                               TaxData,
                               OfferData,
                               SuggestedHotelInfo,
                               ResponseHotel,
                               SuggestedRoomInfo,
                               SuggestedRateInfo)
from common.utils import to_float, to_int, convert_string_to_date, to_decimal, get_total_amount
from content.hotelbeds.types import HbCurrencies, HbRooms, HbBoards
from content.hotelbeds.hotels import HbHotels
from common.decorators import check_null
from common.types import HttpMethods
from cache_memoize import cache_memoize
from common.utils import string_to_sha256hex
from dataclasses import asdict
from common.utils import generate_unique_id, dataclass_to_doc
from typing import List
from common.extensions import mongo_default_db
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import exceptions


class HbAvailability(Availability):
    # emirate_destinations = [ "AAN", "AE1", "AUH", "DXB", "FJR", "RKT", "SHJ", "UMM" ]

    def __init__(self, filters={}):
        self.config = Config(
            endpoint="/hotel-api/1.0/hotels",
            params=None,
            json=self.parse_filters(filters),
            data=None,
            method=HttpMethods.POST
        )
        self.exclude = filters.get("exclude", [])
        self.collection_name = "search_info"

    def parse_occupancies(self, occupancy):
        result = {
            "rooms": occupancy['rooms'],
            "adults": occupancy['adults'],
            "children": occupancy['children']
        }
        if occupancy.get("paxes"):
            result["paxes"] = [{
                "type": pax.get("type"),
                "age": pax.get("age"),
            } for pax in occupancy.get("paxes")]
        return result

    def parse_filters(self, filters):
        if not filters:
            return None

        params = {
            "stay": {
                "checkIn": str(filters['stay']['check_in']),
                "checkOut": str(filters['stay']['check_out'])
            },
            "occupancies": [self.parse_occupancies(occupancy) for occupancy in filters['occupancies']],
            "days": (filters['stay']['check_out'] - filters['stay']['check_in']).days,
            # "offset": filters.get("offset", 0),
        }

        if filters.get("hotels"):
            params.update(
                {"hotels": {"hotel": [int(hotel) for hotel in filters["hotels"]]}})
        elif filters.get("destinations"):
            params.update({"destinations": [{"code": code}
                          for code in filters["destinations"]]})

        if filters.get("limit"):
            params.update({"limit": filters.get("limit", 10)})

        return params

    @check_null()
    def get_offers_dataclasses(self, offers):
        return [
            OfferData(
                code=offer.get("code"),
                name=offer.get("name"),
                amount=offer.get("amount")
            ) for offer in offers
        ]

    @check_null()
    def get_cancelation_policies_dataclasses(self, cancelation_policies):
        return [
            CancellationPlicyData(
                amount=cancelation_policy.get("amount"),
                from_date=convert_string_to_date(
                    cancelation_policy.get("from"), "%Y-%m-%dT%H:%M:%S%z"),
            ) for cancelation_policy in cancelation_policies
        ]

    @check_null()
    def get_taxes_dataclasses(self, taxes):
        return [
            TaxData(
                included=tax.get("included"),
                amount=to_float(tax.get("amount")),
                currency=HbCurrencies().get_by_code(tax.get("currency")),
                client_amount=to_float(tax.get("clientAmount")),
                client_currency=HbCurrencies().get_by_code(tax.get("clientCurrency")),
            ) for tax in taxes
        ]

    @check_null()
    def get_availablerates_dataclasses(self, available_rates):
        def get_hotel_rate(available_rate):
            return to_float(available_rate.get("sellingRate")) if available_rate.get(
                "sellingRate") else to_float(available_rate.get("net"))

        return [
            RateData(
                rate_key=available_rate.get("rateKey"),
                rate_class=available_rate.get("rateClass"),
                rate_type=available_rate.get("rateType"),
                rate_comments_id=available_rate.get("rateCommentsId"),
                net=to_float(available_rate.get("net")),
                selling_rate=to_float(available_rate.get("sellingRate")),
                hotel_selling_rate=to_float(
                    available_rate.get("hotelSellingRate")),
                commission=to_float(available_rate.get("commission")),
                commission_vat=to_float(available_rate.get("commissionVAT")),
                commission_pct=to_float(available_rate.get("commissionPCT")),
                hotel_mandatory=to_float(available_rate.get("hotelMandatory")),
                hotel_currency=HbCurrencies().get_by_code(available_rate.get("hotelCurrency")),
                hotel_rate=get_hotel_rate(available_rate),
                total_rate=get_total_amount(get_hotel_rate(
                    available_rate), settings.HOTEL_FEE_PERCENTAGE),
                total_rate_per_day=to_decimal(get_total_amount(get_hotel_rate(
                    available_rate), settings.HOTEL_FEE_PERCENTAGE) / self.config.json.get("days", 1)),
                allotment=to_int(available_rate.get("allotment")),
                payment_type=available_rate.get("paymentType"),
                packaging=available_rate.get("packaging"),
                rooms_count=available_rate.get("rooms"),
                adults_count=available_rate.get("adults"),
                children_count=available_rate.get("children"),
                board=HbBoards().get_by_code(available_rate.get("boardCode")),
                cancellation_policies=self.get_cancelation_policies_dataclasses(
                    available_rate.get("cancellationPolicies")),
                tax_info=AvailabilityTaxData(
                    taxes=self.get_taxes_dataclasses(
                        available_rate.get("taxes", {}).get("taxes")),
                    all_included=available_rate.get(
                        "taxes", {}).get("allIncluded")
                ) if available_rate.get("taxes") else None,
                offers=self.get_offers_dataclasses(available_rate.get(
                    "offers")) if available_rate.get("offers") else None
            ) for available_rate in available_rates
        ]

    @check_null()
    def get_suggested_rate(self, available_rates):
        return available_rates[0] if len(available_rates) > 0 else None

    @check_null()
    def get_availablerooms_dataclasses(self, available_rooms):
        rooms = []
        for available_room in available_rooms:
            room = HbRooms().get_by_code(available_room.get("code"))
            available_rates = self.get_availablerates_dataclasses(
                available_room.get("rates"))
            suggested_rate = self.get_suggested_rate(available_rates)
            rooms.append(AvailableRoomData(room=room,
                                           available_rates=available_rates,
                                           suggested_rate=suggested_rate))
        return rooms

    @check_null()
    def get_availablehotels_dataclasses(self, available_hotels):
        return [
            AvailableHotelData(
                min_rate=to_float(available_hotel.get("minRate")),
                max_rate=to_float(available_hotel.get("maxRate")),
                currency=HbCurrencies().get_by_code(available_hotel.get("currency")),
                hotel=HbHotels().get_by_code(
                    available_hotel.get("code"), exclude=self.exclude),
                rooms=self.get_availablerooms_dataclasses(
                    available_hotel.get("rooms")),
            ) for available_hotel in available_hotels
        ]

    @cache_memoize(60*60, args_rewrite=lambda self: f"{str(self.config.json)}_{str(self.exclude)}")
    def remote_search(self):
        result = Availability.search(self)
        hotels = result.get("hotels", {})
        return AvailabilityData(
            check_in=hotels.get("checkIn"),
            check_out=hotels.get("checkOut"),
            total=hotels.get("total"),
            hotels=self.get_availablehotels_dataclasses(
                hotels.get("hotels", []))
        )

    def suggested_room(self, rooms: List[AvailableRoomData]):
        if not rooms:
            return None

        return SuggestedRoomInfo(
            code=rooms[0].room.code,
            description=rooms[0].room.description
        )

    def suggested_rate(self, rooms: List[AvailableRoomData]):
        if not rooms:
            return None

        return SuggestedRateInfo(
            rate_key=rooms[0].suggested_rate.rate_key,
            hotel_rate=rooms[0].suggested_rate.hotel_rate,
            total_rate=rooms[0].suggested_rate.total_rate,
            total_rate_per_day=rooms[0].suggested_rate.total_rate_per_day
        )

    def seggested_item(self, search_id, hotel: AvailableHotelData):
        return SuggestedHotelInfo(
            search_id=search_id,
            item_id=generate_unique_id(),
            hotel=ResponseHotel(code=hotel.hotel.code,
                                name=hotel.hotel.name,
                                description=hotel.hotel.description,
                                destination=hotel.hotel.destination,
                                coordinates=hotel.hotel.coordinates,
                                images=hotel.hotel.images,
                                S2C=hotel.hotel.S2C,
                                active=hotel.hotel.active
                                ),
            room=self.suggested_room(hotel.rooms),
            rate=self.suggested_rate(hotel.rooms),
            min_rate=hotel.min_rate,
            max_rate=hotel.max_rate,
            currency=hotel.currency,
            total_room=len(hotel.rooms)
        )

    def get_active_hotels(self, hotels):
        return [hotel for hotel in hotels if hotel["hotel"]["active"]]

    def create_availability_response(self, hotels):
        hotels = self.get_active_hotels(hotels)

        response = {
            "hotels": hotels[:self.config.json.get("limit", 10)] if (self.config.json and self.config.json.get("limit")) else hotels,
            "total": len(hotels)
        }
        if not hotels:
            raise exceptions.NotFound(
                "There is no available stay for this search! Please change the date or occupancy info and try again.")
            # response["message"] = "There is no available stay for this search! Please change the date or occupancy info and try again."

        return response

    def hotel_update_reservation(self, hotels, reservation_info, search_param):
        if not hotels:
            return

        hotel = hotels[0]

        hotel_amount = to_decimal(hotel.get("rate", {}).get("hotel_rate"))
        hotel_fee_amount = to_decimal(hotel.get("rate", {}).get(
            "hotel_rate") * settings.HOTEL_FEE_PERCENTAGE/100)
        total_hotel_amount = to_decimal(hotel_amount + hotel_fee_amount)

        car_amount = to_decimal(reservation_info.car_amount)
        car_fee_amount = to_decimal(reservation_info.car_fee_amount)
        total_car_amount = to_decimal(search_param.get(
            "days") * (car_amount + car_fee_amount))

        total_amount = to_decimal(
            hotel_amount + hotel_fee_amount + (search_param.get("days") * (car_amount + car_fee_amount)))

        reservation_doc = {
            "room_code": hotel.get("room", {}).get("code"),
            "room_description": hotel.get("room", {}).get("description"),
            "rate_key": hotel.get("rate", {}).get("rate_key"),
            "hotel_item_id": hotel.get("item_id"),
            "search": hotel.get("search_params", search_param),
            "total_amount": total_amount,
            "total_hotel_amount": total_hotel_amount,
            "total_car_amount": total_car_amount,
            "hotel_amount": hotel_amount,
            "car_amount": car_amount,
            "hotel_fee_amount": hotel_fee_amount,
            "car_fee_amount": car_fee_amount,
        }

        result = reservation_info.update(reservation_doc)

        return result.to_dict()

    def cache_availability_result(self, data: AvailabilityData, search_id, search_params):
        if not data.hotels:
            return []

        search_response = []

        for hotel in data.hotels:
            item = self.seggested_item(search_id, hotel)
            mongo_item = asdict(item)
            mongo_item["info"] = dataclass_to_doc(hotel)
            mongo_item["search_params"] = search_params
            mongo_item["expiry_date"] = datetime.utcnow(
            ) + timedelta(hours=settings.MONGO_SEARCH_CACHE)
            mongo_default_db["search_info"].insert_one(mongo_item)
            search_response.append(item)

        return search_response

    def get_data_from_mongo(self, search_id):
        result = list(mongo_default_db["search_info"].find(
            {"search_id": search_id}, {"info": 0, "expiry_date": 0, "_id": 0}))

        if not result:
            return None

        return self.create_availability_response(result)

    def search(self):
        search_id = string_to_sha256hex(str(self.config.json))

        # This will return the list of hotels in the chache based on searched id
        result = self.get_data_from_mongo(search_id)

        # If the cache is invalidated or the search is new we will query the hotel Supplier and update our cache
        if not result:
            response_data = self.remote_search()
            search_response = self.cache_availability_result(
                response_data, search_id, self.config.json)
            hotels = [asdict(item) for item in search_response]
            result = self.create_availability_response(hotels)

        return result

    @cache_memoize(10*60, args_rewrite=lambda self: f"{str(self.config.json)}_{str(self.exclude)}")
    def search_v2(self):
        return self.search()

    @cache_memoize(10*60, args_rewrite=lambda self, reservation_info: f"{str(self.config.json)}_{str(reservation_info.id)}")
    def hotel_update_search(self, reservation_info):
        result = self.search()

        # if not result.get("hotels", []):
        #     raise exceptions.NotFound("There is no available stay for this search! Please change the date or occupancy info and try again.")

        updated_reservation = self.hotel_update_reservation(
            result.get("hotels", []), reservation_info, self.config.json)

        return updated_reservation

    def create_new_item(self, item, room, item_id):
        item["item_id"] = generate_unique_id()
        item["search_id"] = item_id + "_OTHER_ROOMS"
        item["room"] = {
            "code": room.get("room", {}).get("code"),
            "description": room.get("room", {}).get("description"),
        }
        item["rate"] = {
            "rate_key": room.get("suggested_rate", {}).get("rate_key"),
            "total_rate": room.get("suggested_rate", {}).get("total_rate"),
            "hotel_rate": room.get("suggested_rate", {}).get("hotel_rate"),
            "total_rate_per_day": room.get("suggested_rate", {}).get("total_rate_per_day"),
        }
        item.pop("_id", None)
        mongo_default_db["search_info"].insert_one(item)

    def create_other_rooms(self, item_id):
        item = mongo_default_db["search_info"].find_one(
            {"item_id": item_id}, {"_id": 0})
        other_rooms = item.get("info", {}).get("rooms", [])
        for room in other_rooms:
            self.create_new_item(item, room, item_id)

    @cache_memoize(10*60, args_rewrite=lambda self, item_id: f"{str(item_id)}")
    def hotel_other_rooms_search(self, item_id):
        result = self.get_data_from_mongo(item_id + "_OTHER_ROOMS")

        if not result:
            self.create_other_rooms(item_id)
            result = self.get_data_from_mongo(item_id + "_OTHER_ROOMS")

        return result
