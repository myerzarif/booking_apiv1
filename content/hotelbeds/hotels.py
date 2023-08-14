from .config import Config
from common.extensions import mongo_default_db
from common.types import Coordinates, Address, Phone
from content.general.models import HotelData, HotelRoomData
from .locations import HbDestinations
from common.utils import convert_string_to_date
from .types import (
    HbCategories,
    HbChains,
    HbAccommodations,
    HbBoards,
    HbSegments,
    HbRooms,
    HbTerminals,
    HbFacilities
)
from content.general.hotels import (
    Hotels,
    HotelDetails,
)


class HbHotels(Hotels):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/hotels",
            params={
                "fields": "all",
                "language": "ENG",
                "useSecondaryLanguage": False,
                "from": 1,
                "to": 1000,
                "countryCode": "AE",
            })
        self.collection_name = self.get_collection_name()

    def convert_phones(self, phones):
        return [Phone(number=phone.get("phoneNumber"), type=phone.get("phoneType")) for phone in phones]

    def get_by_code(self, code):
        doc = self.get_doc_by_code(int(code))
        return HotelData(
            code=doc.get("code"),
            name=doc.get("name", {}).get("content"),
            description=doc.get("description", {}).get("content"),
            destination=HbDestinations().get_by_destination_info(
                doc.get("destinationCode"),
                doc.get("stateCode"),
                doc.get("zoneCode")
            ),
            coordinates=Coordinates(
                longitude=doc.get("coordinates", {}).get("longitude"),
                latitude=doc.get("coordinates", {}).get("latitude")
            ),
            category=HbCategories().get_by_code(doc.get("categoryCode")),
            chain=HbChains().get_by_code(doc.get("chainCode")),
            accommodation=HbAccommodations().get_by_code(doc.get("accommodationTypeCode")),
            boards=HbBoards().get_by_codes(doc.get("boardCodes")),
            segments=HbSegments().get_by_codes(doc.get("segmentCodes")),
            address=Address(
                content=doc.get("content"),
                street=doc.get("street"),
                number=doc.get("number")
            ),
            postal_code=doc.get("postalCode"),
            city=doc.get("city", {}).get("content"),
            email=doc.get("email"),
            phones=self.convert_phones(doc.get("phones")),
            rooms=HbRooms().get_hotelrooms_dataclasses(doc.get("rooms")),
            facilities=HbFacilities().get_roomfacilities_dataclasses(doc.get("facilities")),
            terminals=HbTerminals().get_hotelterminals_by_docs(doc.get("terminals")),
            interest_points=None,
            images=None,
            web=doc.get("web"),
            last_update=convert_string_to_date(
                doc.get("lastUpdate"), "%Y-%m-%d"),
            S2C=doc.get("S2C"),
            ranking=doc.get("ranking")
        )


class HbHotelDetails(HotelDetails):

    def __init__(self, hotelCode):
        self.config = Config(endpoint="/hotel-content-api/1.0/hotels/{}/details".format(hotelCode),
                             params={
                                 "fields": "all",
                                 "language": "ENG",
                                 "useSecondaryLanguage": False
        })
        self.collection_name = self.get_collection_name()
