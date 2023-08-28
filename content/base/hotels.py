
from .content import Content
from common.extensions import mongo_default_db


class Hotels(Content):
    # def __init__(self, **kwargs):
    #     self.code = kwargs["code"]

    def get_collection_name(self):
        return "hotels"

    # def find_hotel_by_code(self, code):
    #     return mongo_default_db[self.collection_name].find({"code": code})


class HotelDetails(Content):

    def get_collection_name(self):
        return "hotels"
