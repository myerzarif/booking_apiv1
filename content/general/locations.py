
from .content import Content


class Countries(Content):

    def get_collection_name(self):
        return "countries"


class Destinations(Content):
    
    def get_collection_name(self):
        return "destinations"