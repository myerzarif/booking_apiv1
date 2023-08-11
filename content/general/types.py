
from .content import Content


class Accommodations(Content):

    def get_collection_name(self):
        return "accommodations"


class Boards(Content):

    def get_collection_name(self):
        return "boards"


class Categories(Content):

    def get_collection_name(self):
        return "categories"


class Chains(Content):

    def get_collection_name(self):
        return "chains"


class Currencies(Content):

    def get_collection_name(self):
        return "currencies"


class Facilities(Content):

    def get_collection_name(self):
        return "facilities"


class FacilityGroups(Content):

    def get_collection_name(self):
        return "facilityGroups"


class FacilityTypologies(Content):

    def get_collection_name(self):
        return "facilityTypologies"


class Issues(Content):

    def get_collection_name(self):
        return "issues"


class Languages(Content):


    def get_collection_name(self):
        return "languages"


class Promotions(Content):

    def get_collection_name(self):
        return "promotions"


class Rooms(Content):

    def get_collection_name(self):
        return "rooms"


class Segments(Content):

    def get_collection_name(self):
        return "segments"


class Terminals(Content):

    def get_collection_name(self):
        return "terminals"


class ImageTypes(Content):

    def get_collection_name(self):
        return "imageTypes"


class GroupCategories(Content):

    def get_collection_name(self):
        return "groupCategories"


class RateComments(Content):

    def get_collection_name(self):
        return "rateComments"


class RateCommentDetails(Content):

    def get_collection_name(self):
        return "rateCommentDetails"
