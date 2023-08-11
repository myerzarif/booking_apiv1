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


class HbAccommodations(Accommodations):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/accommodations")
        self.collection_name = self.get_collection_name()


class HbBoards(Boards):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/boards")
        self.collection_name = self.get_collection_name()


class HbCategories(Categories):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/categories")
        self.collection_name = self.get_collection_name()


class HbChains(Chains):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/chains")
        self.collection_name = self.get_collection_name()


class HbCurrencies(Currencies):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/currencies")
        self.collection_name = self.get_collection_name()


class HbFacilities(Facilities):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/facilities")
        self.collection_name = self.get_collection_name()


class HbFacilityGroups(FacilityGroups):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/facilitygroups")
        self.collection_name = self.get_collection_name()


class HbFacilityTypologies(FacilityTypologies):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/facilitytypologies")
        self.collection_name = self.get_collection_name()


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


class HbSegments(Segments):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/segments")
        self.collection_name = self.get_collection_name()


class HbTerminals(Terminals):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/terminals")
        self.collection_name = self.get_collection_name()


class HbImageTypes(ImageTypes):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/imagetypes")
        self.collection_name = self.get_collection_name()


class HbGroupCategories(GroupCategories):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/groupcategories")
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
