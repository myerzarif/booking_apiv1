from .config import Config
from content.general.hotels import (
    Hotels,
    HotelDetails,
)


class HbHotels(Hotels):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/hotels",
            params={
                "fields": "all",
                "language": "ENG",
                "useSecondaryLanguage": False,
                "from": 1,
                "to": 1000,
                "countryCode": "AE",
            })
        self.collection_name = self.get_collection_name()



class HbHotelDetails(HotelDetails):

    def __init__(self, hotelCode):
        self.config = Config(endpoint="/hotel-content-api/1.0/hotels/{}/details".format(hotelCode),
                             params={
                                 "fields": "all",
                                 "language": "ENG",
                                 "useSecondaryLanguage": False
                             })
        self.collection_name = self.get_collection_name()