from django.core.cache import cache
from django.conf import settings
import logging

LIMIT_UPLOAD_PER_HOUR_BYTES = settings.LIMIT_UPLOAD_PER_HOUR_BYTES
LIMIT_UPLOAD_PER_DAY_BYTES = settings.LIMIT_UPLOAD_PER_DAY_BYTES

DAY_SECONDS = 86400  # 24*60*60 -> 1 day
HOUR_SECONDS = 3600  # 60*60 -> 1 hour

logger = logging.getLogger('project.ratelimit.alert')

def is_limit_upload_file(username, size):
    # per hour check
    added_hour = cache.add(
        f"RATE_LIMIT_UPLOAD_HOUR_{username}", size, HOUR_SECONDS)
    if added_hour:
        size_byte = size
    else:
        size_byte = cache.incr(f"RATE_LIMIT_UPLOAD_HOUR_{username}", size)
    if size_byte >= LIMIT_UPLOAD_PER_HOUR_BYTES:
        return True
    # per day check
    added_day = cache.add(
        f"RATE_LIMIT_UPLOAD_DAY_{username}", size, DAY_SECONDS)
    if added_day:
        size_byte = size
    else:
        size_byte = cache.incr(f"RATE_LIMIT_UPLOAD_DAY_{username}", size)
    if size_byte >= LIMIT_UPLOAD_PER_DAY_BYTES:
        return True
    return False