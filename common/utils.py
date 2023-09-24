"""
Utilty Module of Account App
"""

from uuid import uuid4
import random
import string
import time
import hashlib
import json
import math
from dataclasses import asdict
from datetime import datetime
from random import randint, randrange
import logging

logger = logging.getLogger('project.common')


def generate_unique_id():
    return str(uuid4())


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_strong_password():
    pronounciations = '()#!*+$&_'
    random_source = string.ascii_letters + string.digits + pronounciations
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += random.choice(pronounciations)

    for i in range(6):
        password += random.choice(random_source)

    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password


def get_current_time_in_second():
    # get current time in seconds as integer
    return int(round(time.time()))


def string_to_sha256hex(text):
    sha256 = hashlib.sha256(text.encode('UTF-8'))
    return sha256.hexdigest()


def dataclass_to_json(instance):
    # Convert the data class instance to a dictionary
    data_dict = asdict(instance)

    # Convert the dictionary to JSON
    return json.dumps(data_dict)


def convert_string_to_date(date_str, format_str):
    if not date_str:
        return None

    return datetime.strptime(date_str, format_str).date()


def convert_string_to_datetime(datetime_str, format_str):
    if not datetime_str:
        return None

    return datetime.strptime(datetime_str, format_str)


def random_otp_generator():
    return str(randint(1, 10)) + str(randrange(1000, 9999))


def to_float(value):
    if not value:
        return None

    try:
        return float(value)

    except Exception as e:
        logger.error("invalid float number: exception: {}".format(str(e)))


def to_int(value):
    if not value:
        return None

    try:
        return int(value)

    except Exception as e:
        logger.error("invalid int number: exception: {}".format(str(e)))


def generate_random_string(length=20):
    random_source = string.ascii_letters + string.digits
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)

    for i in range(length-3):
        password += random.choice(random_source)

    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password