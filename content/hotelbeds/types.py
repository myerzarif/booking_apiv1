from content.general.types import (
    Accomodation,
    Boards,
    Categories,
    Chains,
    Currencies,
    Facilities,
    FacilityGroups,
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


class HbAccomodation(Accomodation):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/accommodations")


class HbBoards(Boards):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/boards")


class HbCategories(Categories):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/categories")


class HbChains(Chains):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/chains")


class HbCurrencies(Currencies):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/currencies")


class HbFacilities(Facilities):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/facilities")


class HbFacilityGroups(FacilityGroups):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/facilitygroups")


class HbIssues(Issues):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/issues")


class HbLanguages(Languages):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/languages")


class HbPromotions(Promotions):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/promotions")


class HbRooms(Rooms):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/rooms")


class HbSegments(Segments):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/segments")


class HbTerminals(Terminals):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/types/terminals")


class HbImageTypes(ImageTypes):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/imagetypes")


class HbGroupCategories(GroupCategories):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/groupcategories")


class HbRateComments(RateComments):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/ratecomments")


class HbRateCommentDetails(RateCommentDetails):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/types/ratecommentdetails")
