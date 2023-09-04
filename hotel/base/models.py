from dataclasses import dataclass
from typing import List
from common.types import Coordinates, Address, Phone
from datetime import date, datetime
from content.base.models import HotelData, CurrencyData, RoomData, BoardData


# @dataclass
# class PaxData:
#     type: str
#     age: int


# @dataclass
# class OccupancyData:
#     rooms: int
#     adults: int
#     children: int
#     paxes: List[PaxData]


# @dataclass
# class Stay:
#     check_in: date
#     check_out: date


# @dataclass
# class AvailabilityQueryData:
#     stay: Stay
#     destinations: List[str]
#     occupancies: List[OccupancyData]


@dataclass
class CancellationPlicyData:
    amount: float
    from_date: datetime


@dataclass
class TaxData:
    included: bool
    amount: float
    currency: CurrencyData
    client_amount: float
    client_currency: CurrencyData


@dataclass
class AvailabilityTaxData:
    taxes: List[TaxData]
    all_included: bool


@dataclass
class OfferData:
    code: str
    name: str
    amount: float


@dataclass
class RateData:
    rate_key: str
    rate_class: str
    rate_type: str
    rate_comments_id: str
    net: float
    selling_rate: float
    hotel_selling_rate: float
    hotel_currency: float
    commission: float
    commission_vat: float
    commission_pct: float
    total_rate: float
    hotel_mandatory: bool
    allotment: int
    payment_type: str
    packaging: bool
    board: BoardData
    cancellation_policies: List[CancellationPlicyData]
    tax_info: AvailabilityTaxData
    rooms_count: int
    adults_count: int
    children_count: int
    offers: List[OfferData]


@dataclass
class AvailableRoomData:
    room: RoomData
    available_rates: List[RateData]
    suggested_rate: RateData


@dataclass
class AvailableHotelData:
    hotel: HotelData
    rooms: List[AvailableRoomData]
    min_rate: float
    max_rate: float
    currency: CurrencyData


@dataclass
class AvailabilityData:
    check_in: date
    check_out: date
    total: int
    hotels: List[AvailableHotelData]
