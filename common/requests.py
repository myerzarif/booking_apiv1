from datetime import datetime
import requests as main_requests
import json
import logging
from .types import HttpMethods

logger = logging.getLogger('project.request')


class Request(object):

    def log(func):
        def decorated_function(*args, **kwargs):
            request_time = datetime.now()

            response = func(*args, **kwargs)

            response_time = datetime.now()
            call_duration = (response_time - request_time).total_seconds()
            response = response
            api_name = response.url.split("?")[0].split('/')[-1]

            extra = {
                "request_time": request_time,
                "response_time": response_time,
                "call_duration": call_duration,
                "response_data": str(response.json())[:1000],
                "status_code": response.status_code,
                "api_name": api_name
            }

            logger.info(
                msg="API_REQUEST_RESPONSE",
                extra=extra
            )

            return response
        return decorated_function

    @log
    def get(
        self,
        url: str,
        params: dict = None,
        **kwargs
    ) -> main_requests.Response:
        response = main_requests.get(url, params=params, **kwargs)
        return response

    @log
    def post(
        self,
        url: str,
        data: any = None,
        json: dict = None,
        **kwargs
    ) -> main_requests.Response:
        response = main_requests.post(url, data=data, json=json, **kwargs)
        return response

    @log
    def put(
        self,
        url: str,
        data: any = None,
        **kwargs
    ) -> main_requests.Response:
        response = main_requests.put(url, data=data, **kwargs)
        return response

    @log
    def patch(
        self,
        url: str,
        data: any = None,
        **kwargs
    ) -> main_requests.Response:
        response = main_requests.patch(url, data=data, **kwargs)
        return response

    @log
    def delete(
        self,
        url: str,
        **kwargs
    ) -> main_requests.Response:
        response = main_requests.delete(url, **kwargs)
        return response

    def send_request(self,
                     url: str,
                     method: HttpMethods,
                     params: dict = None,
                     data: any = None,
                     json: dict = None,
                     **kwargs
                     ) -> main_requests.Response:

        if method == HttpMethods.GET:
            return self.get(url=url, params=params, **kwargs)

        if method == HttpMethods.POST:
            return self.post(url=url, data=data, json=json, **kwargs)

        if method == HttpMethods.PUT:
            return self.put(url=url, data=data, **kwargs)

        if method == HttpMethods.PATCH:
            return self.patch(url=url, data=data, **kwargs)

        if method == HttpMethods.DELETE:
            return self.delete(url=url, **kwargs)


requests = Request()
