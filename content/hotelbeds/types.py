from content.general.types import (
    Accommodations,
    Boards,
    Categories,
    Chains,
    Currencies,
    Facilities,
    FacilityGroups,
    FacilityTypologies,
    Issues,
    Languages,
    Promotions,
    Rooms,
    Segments,
    Terminals,
    ImageTypes,
    GroupCategories,
    RateComments,
    RateCommentDetails
)
from .config import Config
from common.extensions import mongo_default_db
from .locations import HbCountries
from content.general.models import (
    CategoryData,
    GroupCategoryData,
    ChainData,
    AccommodationData,
    BoardData,
    SegmentData,
    RoomData,
    HotelRoomData,
    RoomFacilityData,
    FacilityData,
    RoomStayData,
    FacilityGroupData,
    FacilityTypologyData,
    TerminalData,
    HotelTerminalData,
    InterestPointData
)


class HbAccommodations(Accommodations):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/accommodations")
        self.collection_name = self.get_collection_name()

    def get_dataclass_by_doc(self, doc):
        if not doc:
            return None

        return AccommodationData(
            code=doc.get("code"),
            description=doc.get("typeDescription")
        )


class HbBoards(Boards):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/boards")
        self.collection_name = self.get_collection_name()

    def get_dataclass_by_doc(self, doc):
        if not doc:
            return None
        return BoardData(
            code=doc.get("code"),
            description=doc.get("description", {}).get("content"),
        )

    def get_dataclasses_by_docs(self, docs):
        if not docs:
            return None
        return [self.get_dataclass_by_doc(doc) for doc in docs]


class HbGroupCategories(GroupCategories):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/groupcategories")
        self.collection_name = self.get_collection_name()

    def get_dataclass_by_doc(self, doc):
        if not doc:
            return None

        return GroupCategoryData(
            code=doc.get("code"),
            name=doc.get("name", {}).get("content"),
            description=doc.get("description", {}).get("content"),
            order=doc.get("order")
        )


class HbCategories(Categories):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/categories")
        self.collection_name = self.get_collection_name()

    def get_dataclass_by_doc(self, doc):
        if not doc:
            return None

        return CategoryData(
            code=doc.get("code"),
            description=doc.get("description", {}).get("content"),
            group=HbGroupCategories().get_by_code(doc.get("group")))


class HbChains(Chains):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/chains")
        self.collection_name = self.get_collection_name()

    def get_dataclass_by_doc(self, doc):
        if not doc:
            return None

        return ChainData(
            code=doc.get("code"),
            description=doc.get("description", {}).get("content")
        )


class HbCurrencies(Currencies):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/currencies")
        self.collection_name = self.get_collection_name()


class HbFacilityGroups(FacilityGroups):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/facilitygroups")
        self.collection_name = self.get_collection_name()

    def get_dataclass_by_doc(self, doc):
        if not doc:
            return None

        return FacilityGroupData(
            code=str(doc.get("code")),
            description=doc.get("description", {}).get("content")
        )


class HbFacilityTypologies(FacilityTypologies):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/facilitytypologies")
        self.collection_name = self.get_collection_name()

    def get_dataclass_by_doc(self, doc):
        if not doc:
            return None

        return FacilityTypologyData(
            code=str(doc.get("code")),
            number_flag=doc.get("numberFlag"),
            logic_flag=doc.get("logicFlag"),
            fee_flag=doc.get("feeFlag"),
            distance_flag=doc.get("distanceFlag"),
            age_from_flag=doc.get("ageFromFlag"),
            age_to_flag=doc.get("ageToFlag"),
            date_from_flag=doc.get("dateFromFlag"),
            date_to_flag=doc.get("dateToFlag"),
            time_from_flag=doc.get("timeFromFlag"),
            time_to_flag=doc.get("timeToFlag"),
            ind_yes_or_no_flag=doc.get("indYesOrNoFlag"),
            amount_flag=doc.get("amountFlag"),
            currency_flag=doc.get("currencyFlag"),
            app_type_flag=doc.get("appTypeFlag"),
            text_flag=doc.get("textFlag")
        )


class HbFacilities(Facilities):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/facilities")
        self.collection_name = self.get_collection_name()

    def get_roomstays_dataclasses(self, room_stays):
        if not room_stays:
            return None

        return [RoomStayData(
                facilities=self.get_roomfacilities_dataclasses(
                    room_stay.get("roomStayFacilities")),
                type=room_stay.get("stayType"),
                order=int(room_stay.get("order")),
                description=room_stay.get("description")
                ) for room_stay in room_stays]

    def get_roomfacilities_dataclasses(self, room_facilities):
        if not room_facilities:
            return None

        return [RoomFacilityData(
                facility=self.get_by_info(roomfacility.get(
                    "facilityCode"), roomfacility.get("facilityGroupCode")),
                ind_logic=roomfacility.get("indLogic"),
                ind_fee=roomfacility.get("indFee"),
                ind_yes_or_no=roomfacility.get("indYesOrNo"),
                number=roomfacility.get("number"),
                voucher=roomfacility.get("voucher"),
                time_from=roomfacility.get("timeFrom"),
                time_to=roomfacility.get("timeTo"),
                ) for roomfacility in room_facilities]

    def get_dataclass_by_doc(self, doc):
        if not doc:
            return None

        return FacilityData(
            code=str(doc.get("code")),
            description=doc.get("description", {}).get("content"),
            group=HbFacilityGroups().get_by_code(doc.get("facilityGroupCode")),
            typology=HbFacilityTypologies().get_by_code(doc.get("facilityTypologyCode"))
        )

    def get_by_info(self, facility_code, facility_group_code):
        if not facility_code or not facility_group_code:
            return None

        doc = mongo_default_db[self.collection_name].find_one(
            {"code": int(facility_code), "facilityGroupCode": int(facility_group_code)})

        return self.get_dataclass_by_doc(doc)


class HbIssues(Issues):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/issues")
        self.collection_name = self.get_collection_name()


class HbLanguages(Languages):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/languages")
        self.collection_name = self.get_collection_name()


class HbPromotions(Promotions):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/promotions")
        self.collection_name = self.get_collection_name()


class HbRooms(Rooms):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/rooms")
        self.collection_name = self.get_collection_name()

    def get_hotelrooms_dataclasses(self, hotelrooms):
        if not hotelrooms:
            return None

        return [HotelRoomData(
                is_parent_romm=hotelroom.get("isParentRoom"),
                pms_room_code=hotelroom.get("PMSRoomCode"),
                room_info=self.get_by_code(hotelroom.get("roomCode")),
                facilities=HbFacilities().get_roomfacilities_dataclasses(
                    hotelroom.get("roomFacilities")),
                room_stays=HbFacilities().get_roomstays_dataclasses(hotelroom.get("roomStays"))
                ) for hotelroom in hotelrooms]

    def get_dataclass_by_doc(self, doc):
        if not doc:
            return None

        return RoomData(
            code=doc.get("code"),
            description=doc.get("description"),
            type=doc.get("type"),
            characteristic=doc.get("characteristic"),
            type_description=doc.get("typeDescription", {}).get("content"),
            characteristic_description=doc.get(
                "characteristicDescription", {}).get("content"),
            min_pax=doc.get("minPax"),
            max_pax=doc.get("maxPax"),
            min_adults=doc.get("minAdults"),
            max_adults=doc.get("maxAdults"),
            max_children=doc.get("maxChildren"),
        )

    def get_dataclasses_by_docs(self, docs):
        if not docs:
            return None

        return [self.get_dataclass_by_doc(doc) for doc in docs]


class HbSegments(Segments):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/segments")
        self.collection_name = self.get_collection_name()

    def get_dataclass_by_doc(self, doc):
        if not doc:
            return None

        return SegmentData(
            code=str(doc.get("code")),
            description=doc.get("description", {}).get("content"),
        )

    def get_dataclasses_by_docs(self, docs):
        if not docs:
            return None

        return [self.get_dataclass_by_doc(doc) for doc in docs]

    def get_by_codes(self, codes):
        if not codes:
            return None

        codes = [str(code) for code in codes]
        docs = self.get_docs_by_codes(codes)
        return self.get_dataclasses_by_docs(docs)


class HbTerminals(Terminals):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/terminals")
        self.collection_name = self.get_collection_name()

    def get_dataclass_by_doc(self, doc):
        if not doc:
            return None

        return TerminalData(
            code=doc.get("code"),
            name=doc.get("name", {}).get("content"),
            description=doc.get("description", {}).get("content"),
            type=doc.get("type"),
            country=HbCountries().get_by_code(doc.get("country"))
        )

    def get_hotelterminals_by_docs(self, terminals):
        if not terminals:
            return None

        return [HotelTerminalData(
                terminal=self.get_by_code(terminal.get("terminalCode")),
                distance=terminal.get("distance"),
                ) for terminal in terminals]


class HbImageTypes(ImageTypes):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/imagetypes")
        self.collection_name = self.get_collection_name()


class HbRateComments(RateComments):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/ratecomments")
        self.collection_name = self.get_collection_name()


class HbRateCommentDetails(RateCommentDetails):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/ratecommentdetails")
        self.collection_name = self.get_collection_name()
