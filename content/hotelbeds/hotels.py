from .config import Config
from common.extensions import mongo_default_db
from common.types import Coordinates, Address, Phone
from content.base.models import HotelData, HotelRoomData
from .locations import HbDestinations
from common.utils import convert_string_to_date
from dataclasses import asdict
from rest_framework.exceptions import NotFound
from cache_memoize import cache_memoize
from .types import (
    HbCategories,
    HbChains,
    HbAccommodations,
    HbBoards,
    HbSegments,
    HbRooms,
    HbTerminals,
    HbFacilities,
    HbImageTypes
)
from content.base.hotels import (
    Hotels,
    HotelDetails,
)
from common.utils import to_int

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

    def get_dataclass_by_doc_limited(self, doc):
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
            category=None,
            chain=None,
            accommodation=None,
            boards=None,
            segments=None,
            address=Address(
                content=doc.get("address", {}).get("content"),
                street=doc.get("address", {}).get("street"),
                number=doc.get("address", {}).get("number")
            ),
            postal_code=doc.get("postalCode"),
            city=doc.get("city", {}).get("content"),
            email=doc.get("email"),
            phones=self.convert_phones(doc.get("phones")),
            rooms=None,
            facilities=None,
            terminals=None,
            interest_points=None,
            images=None,
            web=doc.get("web"),
            last_update=None,
            S2C=doc.get("S2C"),
            ranking=doc.get("ranking")
        )

    def get_dataclass_by_doc(self, doc, exclude=[]):
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
                content=doc.get("address", {}).get("content"),
                street=doc.get("address", {}).get("street"),
                number=doc.get("address", {}).get("number")
            ),
            postal_code=doc.get("postalCode"),
            city=doc.get("city", {}).get("content"),
            email=doc.get("email"),
            phones=self.convert_phones(doc.get("phones")),
            rooms=HbRooms().get_hotelrooms_dataclasses(
                doc.get("rooms")) if "rooms" not in exclude else None,
            facilities=HbFacilities().get_roomfacilities_dataclasses(
                doc.get("facilities")) if "facilities" not in exclude else None,
            terminals=HbTerminals().get_hotelterminals_by_docs(doc.get("terminals")),
            interest_points=HbFacilities().get_interestpoints_dataclasses(
                doc.get("interestPoints")) if "interest_points" not in exclude else None,
            images=HbImageTypes().get_hotelimages_dataclasses(
                doc.get("images")) if "images" not in exclude else None,
            web=doc.get("web"),
            last_update=convert_string_to_date(
                doc.get("lastUpdate"), "%Y-%m-%d"),
            S2C=doc.get("S2C"),
            ranking=doc.get("ranking")
        )

    def get_by_code(self, code, exclude=[]):
        doc = self.get_doc_by_code(int(code))
        if not doc:
            raise NotFound("Hotel not found!")

        return self.get_dataclass_by_doc(code, exclude=[])
    
    def search(self, params):
        filters = {}

        if params.get("code"):
            filters.update(
                {"code": to_int(params.get("code"))}
            )

        if params.get("name"):
            filters.update(
                {"name.content": params.get("name")}
            )

        if params.get("offset") and params.get("limit"):
            return [asdict(self.get_dataclass_by_doc_limited(item)) for item in list(mongo_default_db[self.collection_name].find(filters).skip(params.get("offset")).limit(params.get("limit")))]
        
        return [asdict(self.get_dataclass_by_doc_limited(item)) for item in list(mongo_default_db[self.collection_name].find(filters))]


class HbHotelDetails(HotelDetails):

    def __init__(self, hotelCode):
        self.config = Config(endpoint="/hotel-content-api/1.0/hotels/{}/details".format(hotelCode),
                             params={
                                 "fields": "all",
                                 "language": "ENG",
                                 "useSecondaryLanguage": False
        })
        self.collection_name = self.get_collection_name()


