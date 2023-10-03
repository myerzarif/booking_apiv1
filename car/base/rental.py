from common.requests import requests
from common.extensions import mongo_default_db
from common.exceptions import ThirdPartyAPIFailure
from common.decorators import check_null
import logging
from cache_memoize import cache_memoize
import pymongo

logger = logging.getLogger('project.car')


logger = logging.getLogger('project.hotel')


class Rental():
    def rent(self):
        response = requests.send_request(url=self.config.base_url + self.config.endpoint,
                                         method=self.config.method,
                                         params=self.config.params,
                                         data=self.config.data,
                                         json=self.config.json,
                                         headers=self.config.headers,
                                         timeout=50
                                         )
        if not response.ok:
            logger.error("failed to call rental api", extra={
                         "code": response.status_code, "text": response.text})
            raise ThirdPartyAPIFailure

        return response.json()

    @cache_memoize(60*60*24, args_rewrite=lambda self, code: f"{code}_{str(self)}")
    @check_null()
    def get_doc_by_code(self, code):
        return mongo_default_db[self.collection_name].find_one({"code": code})

    @cache_memoize(60*60*24, args_rewrite=lambda self, codes: f"{str(codes)}_{str(self)}")
    @check_null()
    def get_docs_by_codes(self, codes):
        return list(mongo_default_db[self.collection_name].find({"code": {'$in': codes}}))

    @check_null()
    def get_by_code(self, code):
        doc = self.get_doc_by_code(code)
        return self.get_dataclass_by_doc(doc)

    def get_by_codes(self, codes):
        docs = self.get_docs_by_codes(codes)
        return self.get_dataclasses_by_docs(docs)

    def __str__(self):
        return self.collection_name
