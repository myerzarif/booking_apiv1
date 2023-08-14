
from .content import Content
from dataclasses import dataclass
from typing import List


class Countries(Content):

    def get_collection_name(self):
        return "countries"


class Destinations(Content):

    def get_collection_name(self):
        return "destinations"
