
from .content import Content


class Hotels(Content):

    def get_collection_name(self):
        return "hotels"


class HotelDetails(Content):
    
    def get_collection_name(self):
        return "hotels"