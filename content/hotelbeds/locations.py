from .config import Config
from common.extensions import mongo_default_db
from content.general.models import DestinationData, CountryData, ZoneData, StateData
from common.decorators import check_null
from content.general.locations import (
    Countries,
    Destinations,
)


class HbCountries(Countries):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/locations/countries")
        self.collection_name = self.get_collection_name()

    def get_state(self, states, state_code):
        for item in states:
            if item.get("code") == state_code:
                return StateData(
                    code=item.get("code"),
                    name=item.get("name")
                )
        return None

    @check_null(['doc'])
    def get_dataclass_by_doc(self, doc, state_code=None):
        return CountryData(
            code=doc.get("code"),
            name=doc.get("description", {}).get("content"),
            state=self.get_state(
                doc.get("states"), state_code) if state_code else None
        )

    def get_by_country_info(self, country_code, state_code):
        doc = self.get_doc_by_code(country_code)
        return self.get_dataclass_by_doc(doc, state_code)


class HbDestinations(Destinations):

    def __init__(self):
        self.config = Config(
            endpoint="/hotel-content-api/1.0/locations/destinations")
        self.collection_name = self.get_collection_name()

    def get_zone(self, zones, zone_code):
        for item in zones:
            if item.get("zoneCode") == zone_code:
                return ZoneData(
                    code=item.get("zoneCode"),
                    name=item.get("name"),
                    description=item.get("description", {}).get("content"),
                )
        return None

    @check_null(['doc'])
    def get_dataclass_by_doc(self, doc, state_code, zone_code):
        return DestinationData(
            code=doc.get("code"),
            name=doc.get("name", {}).get("content"),
            country=HbCountries().get_by_country_info(doc.get("countryCode"), state_code),
            zone=self.get_zone(doc.get("zones"), zone_code)
        )

    def get_by_destination_info(self, destination_code, state_code, zone_code):
        doc = self.get_doc_by_code(destination_code)
        return self.get_dataclass_by_doc(doc, state_code, zone_code)
