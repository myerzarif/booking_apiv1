from common.extensions import mongo_default_db
from common.decorators import check_null
from .config import Config
from .locations import HbCountries
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
    InterestPointData,
    ImageTypeData,
    ImageData
)


class HbAccommodations(Accommodations):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/accommodations")
        self.collection_name = self.get_collection_name()

    @check_null()
    def get_dataclass_by_doc(self, doc):
        return AccommodationData(
            code=doc.get("code"),
            description=doc.get("typeDescription")
        )


class HbBoards(Boards):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/boards")
        self.collection_name = self.get_collection_name()

    @check_null()
    def get_dataclass_by_doc(self, doc):
        return BoardData(
            code=doc.get("code"),
            description=doc.get("description", {}).get("content"),
        )

    @check_null()
    def get_dataclasses_by_docs(self, docs):
        return [self.get_dataclass_by_doc(doc) for doc in docs]


class HbGroupCategories(GroupCategories):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/groupcategories")
        self.collection_name = self.get_collection_name()

    @check_null()
    def get_dataclass_by_doc(self, doc):
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

    @check_null()
    def get_dataclass_by_doc(self, doc):
        return CategoryData(
            code=doc.get("code"),
            description=doc.get("description", {}).get("content"),
            group=HbGroupCategories().get_by_code(doc.get("group")))


class HbChains(Chains):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/chains")
        self.collection_name = self.get_collection_name()

    @check_null()
    def get_dataclass_by_doc(self, doc):
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

    @check_null()
    def get_dataclass_by_doc(self, doc):
        return FacilityGroupData(
            code=str(doc.get("code")),
            description=doc.get("description", {}).get("content")
        )


class HbFacilityTypologies(FacilityTypologies):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/facilitytypologies")
        self.collection_name = self.get_collection_name()

    @check_null()
    def get_dataclass_by_doc(self, doc):
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

    @check_null()
    def get_interestpoints_dataclasses(self, interest_points):
        return [InterestPointData(
                order=int(interest_point.get("order")),
                name=interest_point.get("poiName"),
                distance=int(interest_point.get("distance")),
                facility=self.get_by_info(
                    interest_point.get("facilityCode"),
                    interest_point.get("facilityGroupCode")
                ),
                ) for interest_point in interest_points]

    @check_null()
    def get_roomstays_dataclasses(self, room_stays):
        return [RoomStayData(
                facilities=self.get_roomfacilities_dataclasses(
                    room_stay.get("roomStayFacilities")
                ),
                type=room_stay.get("stayType"),
                order=int(room_stay.get("order")),
                description=room_stay.get("description")
                ) for room_stay in room_stays]

    @check_null()
    def get_roomfacilities_dataclasses(self, room_facilities):
        return [RoomFacilityData(
                facility=self.get_by_info(
                    roomfacility.get("facilityCode"),
                    roomfacility.get("facilityGroupCode")
                ),
                ind_logic=roomfacility.get("indLogic"),
                ind_fee=roomfacility.get("indFee"),
                ind_yes_or_no=roomfacility.get("indYesOrNo"),
                number=roomfacility.get("number"),
                voucher=roomfacility.get("voucher"),
                time_from=roomfacility.get("timeFrom"),
                time_to=roomfacility.get("timeTo"),
                ) for roomfacility in room_facilities]

    @check_null()
    def get_dataclass_by_doc(self, doc):
        return FacilityData(
            code=str(doc.get("code")),
            description=doc.get("description", {}).get("content"),
            group=HbFacilityGroups().get_by_code(doc.get("facilityGroupCode")),
            typology=HbFacilityTypologies().get_by_code(doc.get("facilityTypologyCode"))
        )

    @check_null()
    def get_by_info(self, facility_code, facility_group_code):
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

    @check_null()
    def get_hotelrooms_dataclasses(self, hotelrooms):
        return [HotelRoomData(
                is_parent_romm=hotelroom.get("isParentRoom"),
                pms_room_code=hotelroom.get("PMSRoomCode"),
                room_info=self.get_by_code(hotelroom.get("roomCode")),
                facilities=HbFacilities().get_roomfacilities_dataclasses(
                    hotelroom.get("roomFacilities")),
                room_stays=HbFacilities().get_roomstays_dataclasses(hotelroom.get("roomStays"))
                ) for hotelroom in hotelrooms]

    @check_null()
    def get_dataclass_by_doc(self, doc):
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

    @check_null()
    def get_dataclasses_by_docs(self, docs):
        return [self.get_dataclass_by_doc(doc) for doc in docs]


class HbSegments(Segments):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/segments")
        self.collection_name = self.get_collection_name()

    @check_null()
    def get_dataclass_by_doc(self, doc):
        return SegmentData(
            code=str(doc.get("code")),
            description=doc.get("description", {}).get("content"),
        )

    @check_null()
    def get_dataclasses_by_docs(self, docs):
        return [self.get_dataclass_by_doc(doc) for doc in docs]

    @check_null()
    def get_by_codes(self, codes):
        docs = self.get_docs_by_codes(codes)
        return self.get_dataclasses_by_docs(docs)


class HbTerminals(Terminals):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/terminals")
        self.collection_name = self.get_collection_name()

    @check_null()
    def get_dataclass_by_doc(self, doc):
        return TerminalData(
            code=doc.get("code"),
            name=doc.get("name", {}).get("content"),
            description=doc.get("description", {}).get("content"),
            type=doc.get("type"),
            country=HbCountries().get_by_code(doc.get("country"))
        )

    @check_null()
    def get_hotelterminals_by_docs(self, terminals):
        return [HotelTerminalData(
                terminal=self.get_by_code(terminal.get("terminalCode")),
                distance=terminal.get("distance"),
                ) for terminal in terminals]


class HbImageTypes(ImageTypes):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/imagetypes")
        self.collection_name = self.get_collection_name()

    @check_null()
    def get_dataclass_by_doc(self, doc):
        return ImageTypeData(
            code=str(doc.get("code")),
            description=doc.get("description", {}).get("content"),
        )

    @check_null()
    def get_hotelimages_dataclasses(self, images):
        return [ImageData(
                type=self.get_by_code(image.get("imageTypeCode")),
                path=image.get("path"),
                order=image.get("order"),
                visual_order=image.get("visualOrder"),
                room=HbRooms().get_by_code(image.get("roomCode"))
                ) for image in images]


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
