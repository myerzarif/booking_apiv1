from common.requests import requests
from common.extensions import mongo_default_db
from common.exceptions import ThirdPartyAPIFailure
import logging

logger = logging.getLogger('project.content')


class Content():

    def daily_update(self):
        print("daily_update")
        return "daily_update"

    def call_initial(self):
        response = requests.send_request(url=self.get_full_url(),
                                         method=self.config.method,
                                         params=self.config.params,
                                         data=self.config.data,
                                         json=self.config.json,
                                         headers=self.config.headers
                                         )
        if not response.ok:
            logger.error("failed to call content apis", extra={
                         "code": response.status_code, "text": response.text})
            raise ThirdPartyAPIFailure

        return response.json()

    def initial_insert(self):
        result = self.call_initial()
        col = self.collection_name
        mongo_default_db[col].insert_many(result.get(col, {}))

    def get_full_url(self):
        return self.config.base_url + self.config.endpoint
