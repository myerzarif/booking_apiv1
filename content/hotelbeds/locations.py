from .config import Config
from content.general.locations import (
    Countries,
    Destinations,
)


class HbCountries(Countries):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/locations/countries",
            params={
                "fields": "all",
                "language": "ENG",
                "from": 1,
                "to": 203
            })


class HbDestinations(Destinations):

    def __init__(self):
        self.config = Config(endpoint="/hotel-content-api/1.0/locations/destinations",
                             params={
                                 "fields": "all",
                                 "language": "ENG",
                                 "from": 1,
                                 "to": 203,
                                 "useSecondaryLanguage": False,
                                 "countryCode": "AE"
                             })
