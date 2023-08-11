"""
List of customize exceptions
with customize text
"""

from rest_framework.exceptions import APIException
from django.utils.translation import ugettext


class ThirdPartyAPIFailure(APIException):
    """
    Error when third party api is not returning success response
    """
    status_code = 500
    default_detail = "Third Party API Failed!"
    default_code = "Third Party API Failed!"