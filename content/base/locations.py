
from .content import Content
from dataclasses import dataclass
from typing import List
from cache_memoize import cache_memoize
from django.conf import settings
import json
import os


class Countries(Content):

    def get_collection_name(self):
        return "countries"


class Destinations(Content):

    def get_collection_name(self):
        return "destinations"


class StaticCountries():

    @cache_memoize(60*60*24*7, args_rewrite=lambda self: f"static_countries")
    def get_static_countries(self):
        with open(settings.BASE_DIR / 'file/statics/countries.json') as json_file:
            return json.load(json_file)
