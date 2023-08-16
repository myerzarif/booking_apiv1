from dataclasses import dataclass
from typing import List
from common.types import Coordinates, Address, Phone
from datetime import date


@dataclass
class AccommodationData:
    code: str
    description: str


@dataclass
class BoardData:
    code: str
    description: str


@dataclass
class GroupCategoryData:
    code: str
    order: int
    name: str
    description: str


@dataclass
class CategoryData:
    code: str
    group: GroupCategoryData
    description: str


@dataclass
class ChainData:
    code: str
    description: str


@dataclass
class SegmentData:
    code: str
    description: str


@dataclass
class FacilityGroupData:
    code: str
    description: str


@dataclass
class FacilityTypologyData:
    code: str
    number_flag: bool
    logic_flag: bool
    fee_flag: bool
    distance_flag: bool
    age_from_flag: bool
    age_to_flag: bool
    date_from_flag: bool
    date_to_flag: bool
    time_from_flag: bool
    time_to_flag: bool
    ind_yes_or_no_flag: bool
    amount_flag: bool
    currency_flag: bool
    app_type_flag: bool
    text_flag: bool


@dataclass
class FacilityData:
    code: str
    description: str
    group: FacilityGroupData
    typology: FacilityTypologyData


@dataclass
class RoomFacilityData:
    facility: FacilityData
    ind_logic: bool
    ind_fee: bool
    ind_yes_or_no: bool
    number: int
    voucher: bool
    time_from: str
    time_to: str


@dataclass
class RoomStayData:
    type: str
    order: int
    description: str
    facilities: List[RoomFacilityData]


@dataclass
class RoomData:
    code: str
    description: str
    type: str
    characteristic: str
    type_description: str
    characteristic_description: str
    min_pax: int
    max_pax: int
    min_adults: int
    max_adults: int
    max_children: int


@dataclass
class HotelRoomData:
    is_parent_romm: bool
    pms_room_code: str
    room_info: RoomData
    facilities: List[RoomFacilityData]
    room_stays: List[RoomStayData]


@dataclass
class ZoneData:
    code: int
    name: str
    description: str


@dataclass
class StateData:
    code: str
    name: str


@dataclass
class CountryData:
    code: str
    name: str
    state: StateData


@dataclass
class DestinationData:
    code: str
    name: str
    country: CountryData
    zone: ZoneData


@dataclass
class TerminalData:
    code: str
    name: str
    description: str
    type: str
    country: CountryData


@dataclass
class HotelTerminalData:
    terminal: TerminalData
    distance: int


@dataclass
class InterestPointData:
    facility: FacilityData
    order: int
    name: str
    distance: int


@dataclass
class ImageTypeData:
    code: str
    description: str


@dataclass
class ImageData:
    type: ImageTypeData
    path: str
    order: int
    visual_order: int
    room: RoomData


@dataclass
class HotelData:
    code: str
    name: str
    description: str
    destination: DestinationData
    coordinates: Coordinates
    category: CategoryData
    chain: ChainData
    accommodation: AccommodationData
    boards: List[BoardData]
    segments: List[SegmentData]
    address: Address
    postal_code: str
    city: str
    email: str
    phones: List[Phone]
    rooms: List[HotelRoomData]
    facilities: List[RoomFacilityData]
    images: List[ImageData]
    web: str
    last_update: date
    S2C: str
    ranking: int
    terminals: str
    interest_points: str
