"""
Signals Account App
Multi Change When new object create or modify
"""

from django.db.models.signals import post_save

from .models import AccessToken
from django.conf import settings


def deactive_access_token(sender, instance, created, **kwargs):
    """
    Deactive access token
    when new accesstoken create : other older access token delete
    """
    if created:
        for origin in settings.CORS_ORIGIN_WHITELIST:
            active_access_token = AccessToken.objects.filter(
                user=instance.user, origin=origin).order_by('-created')[:2]
            AccessToken.objects.exclude(pk__in=active_access_token).filter(
                user=instance.user, origin=origin).update(is_active=False)


post_save.connect(deactive_access_token, sender=AccessToken)
