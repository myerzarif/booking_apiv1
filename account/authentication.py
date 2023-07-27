"""Authentication Module"""
from rest_framework.authentication import TokenAuthentication
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from .models import AccessToken
import hashlib
import logging

logger = logging.getLogger('project.authenticate')


def get_user_agent_header(request):
    """
    Return request's 'User-Agent:' header, as a bytestring.
    """
    user_agent = request.META.get('HTTP_USER_AGENT', b'')
    if isinstance(user_agent, str):
        user_agent = user_agent.encode(HTTP_HEADER_ENCODING)
    return hashlib.sha256(user_agent).hexdigest()


class CustomizeTokenAuthentication(TokenAuthentication):
    """
    Customize class for Token Authentication
    diffrence Between super class : just model
    """
    model = AccessToken

    def authenticate(self, request):
        self.user_agent_hash = get_user_agent_header(request)
        return super(CustomizeTokenAuthentication, self).authenticate(request)

    def authenticate_credentials(self, key):
        """
        check accesstoken and check is active
        """
        model = self.get_model()
        try:
            token = model.objects.select_related(
                'user').get(key=key)
        except model.DoesNotExist:
            logger.info(
                "UNAUTHORIZED :: Token Authentication Not Exist", extra={"key": key})
            raise exceptions.AuthenticationFailed("Token is Incorrect!")

        if not token.user.active:
            logger.info("UNAUTHORIZED :: User of Token Not Active",
                        extra={"key": key, "user": token.user.email})
            raise exceptions.AuthenticationFailed(
                ("Your Account is Deactivated!"))
        if token.isExpire():
            logger.info("UNAUTHORIZED :: Token is Expired",
                        extra={
                            "key": key,
                            "email": token.user.email,
                            "expire_time": token.expire_time,
                            "created_at": token.created_at,
                            "last_modified": token.last_modified,
                        })
            raise exceptions.AuthenticationFailed("Token is Expired!")

        return (token.user, token)
