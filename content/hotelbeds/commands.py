from time import sleep
from .locations import (
    HbCountries,
    HbDestinations
)
from .hotels import (
    HbHotels
)
from .types import (
    HbAccommodations,
    HbBoards,
    HbCategories,
    HbChains,
    HbCurrencies,
    HbFacilities,
    HbFacilityGroups,
    HbFacilityTypologies,
    HbIssues,
    HbLanguages,
    HbPromotions,
    HbRooms,
    HbSegments,
    HbTerminals,
    HbImageTypes,
    HbGroupCategories,
    HbRateComments,
    HbRateCommentDetails
)


def initial_type_insert(_from=None, _to=None):
    hb_classes = [
        HbAccommodations,  # done
        HbBoards,  # done
        HbCategories,  # done
        HbChains,  # done
        HbCurrencies,  # done
        HbFacilities,  # done
        HbFacilityGroups,  # done
        HbFacilityTypologies,  # done
        HbIssues,  # done
        HbLanguages,  # done
        HbPromotions,  # done
        HbRooms,  # done
        HbSegments,  # done
        HbTerminals,  # done
        HbImageTypes,  # done
        HbGroupCategories  # done
    ]

    for cls in hb_classes:
        instance = cls()
        if _from and _to:
            instance.config.params["from"] = _from
            instance.config.params["to"] = _to
        print("instance", instance)
        instance.initial_insert()
        sleep(1)


def initial_location_insert(_from=None, _to=None):
    hb_classes = [HbCountries, HbDestinations]

    for cls in hb_classes:
        instance = cls()
        if _from and _to:
            instance.config.params["from"] = _from
            instance.config.params["to"] = _to
        print("instance", instance)
        instance.initial_insert()
        sleep(1)


def initial_hotel_insert(_from=None, _to=None):
    hb_classes = [HbHotels]

    for cls in hb_classes:
        instance = cls()
        if _from and _to:
            instance.config.params["from"] = _from
            instance.config.params["to"] = _to
        print("instance", instance)
        instance.initial_insert()
        sleep(1)
