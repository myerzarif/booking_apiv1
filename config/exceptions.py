from django.core.exceptions import MiddlewareNotUsed
from rest_framework.exceptions import APIException
import logging


logger = logging.getLogger('project.config')


class ServerError(APIException):
    """
    Error when except unhandle error
    """
    status_code = 500
    default_detail = "Internal Server Error!"
    default_code = "Service is not available!"


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error("unhandledexception: {}".format(str(exception)))
        return ServerError()


class StreamingHttpResponseException(Exception):
    pass
