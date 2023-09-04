from hotel.base.availability import Availability
from content.hotelbeds.config import Config
from hotel.base.models import (AvailabilityData,
                               AvailableHotelData,
                               AvailableRoomData,
                               RateData,
                               CancellationPlicyData,
                               AvailabilityTaxData,
                               TaxData,
                               OfferData)
from common.utils import to_float, convert_string_to_date
from content.hotelbeds.types import HbCurrencies, HbRooms, HbBoards
from content.hotelbeds.hotels import HbHotels
from common.decorators import check_null
from common.types import HttpMethods
from cache_memoize import cache_memoize


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
            "occupancies": [self.parse_occupancies(occupancy) for occupancy in filters['occupancies']]
        }
        if filters["destinations"]:
            params.update({"destinations": [{"code": code}
                          for code in filters["destinations"]]})
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
                total_rate=to_float(available_rate.get("sellingRate")) if available_rate.get(
                    "sellingRate") else to_float(available_rate.get("net")),
                allotment=to_float(available_rate.get("allotment")),
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
    def search(self):
        result = Availability.search(self)
        hotels = result.get("hotels", {})
        return AvailabilityData(
            check_in=hotels.get("checkIn"),
            check_out=hotels.get("checkOut"),
            total=hotels.get("total"),
            hotels=self.get_availablehotels_dataclasses(
                hotels.get("hotels", []))
        )
