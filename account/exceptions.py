"""
List of customize exceptions
with customize text
"""

from rest_framework.exceptions import APIException


class ServerError(APIException):
    """
    Error when except unhandle error
    """
    status_code = 500
    default_detail = "Internal Server Error!"
    default_code = "Service is not available!"
