from .config import Config
from content.general.locations import (
    Countries,
    Destinations,
)


class HbCountries(Countries):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/locations/countries")
        self.collection_name = self.get_collection_name()


class HbDestinations(Destinations):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/locations/destinations")
        self.collection_name = self.get_collection_name()
