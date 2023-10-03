
from common.extensions import mongo_default_db
import logging
from common.requests import requests
from common.exceptions import ThirdPartyAPIFailure

logger = logging.getLogger('project.hotel')


class Availability():
    def search(self):
        response = requests.send_request(url=self.config.base_url + self.config.endpoint,
                                         method=self.config.method,
                                         params=self.config.params,
                                         data=self.config.data,
                                         json=self.config.json,
                                         headers=self.config.headers,
                                         timeout=50
                                         )
        if not response.ok:
            logger.error("failed to call availability api", extra={
                         "code": response.status_code, "text": response.text})
            raise ThirdPartyAPIFailure

        return response.json()

    def get_search_info(self, item_id):
        result = mongo_default_db["search_info"].find_one({"item_id": item_id})
        if not result:
            return None
        
        result.pop("info", None)

        return result