
from common.extensions import mongo_default_db


class Availability():
    # def __init__(self, **kwargs):
    #     self.code = kwargs["code"]

    def get_collection_name(self):
        return "hotels"
