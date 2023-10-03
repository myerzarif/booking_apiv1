from dataclasses import dataclass
from typing import List
from datetime import date
from typing import Literal, Optional


@dataclass
class CarData:
    code: str
    name: str
    description: str
    price: float
    active: bool
    image: str
    type: str
