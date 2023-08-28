from content.base.config import BaseConfig
from django.conf import settings
from common.utils import get_current_time_in_second
from common.utils import string_to_sha256hex
from common.types import HttpMethods


default_params = {"fields": "all",
                  "language": "ENG",
                  "from": 1,
                  "to": 1000,
                  "useSecondaryLanguage": False}


class Config(BaseConfig):

    def __init__(self, endpoint, params=default_params, method=HttpMethods.GET, lastUpdateTime=None):
        self.supplier_name = "hotelbeds"
        self.base_url = settings.HOTELBEDS_BASE_URL
        self.endpoint = endpoint
        self.method = method
        self.params = params
        self.data = None
        self.json = None
        self.lastUpdateTime = lastUpdateTime
        self.headers = self.get_headers()

    def get_headers(self):
        headers = {
            "Api-key": settings.HOTELBEDS_API_KEY,
            "X-Signature": self.generat_signature(),
            "Accept-Encoding": "gzip"
        }

        if self.lastUpdateTime:
            headers["lastUpdateTime"] = self.lastUpdateTime

        return headers

    def generat_signature(self):
        assemble = settings.HOTELBEDS_API_KEY + \
            settings.HOTELBEDS_SECRET + str(get_current_time_in_second())

        return string_to_sha256hex(assemble)
