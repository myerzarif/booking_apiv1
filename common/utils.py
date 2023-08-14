"""
Utilty Module of Account App
"""

from uuid import uuid4
import random
import string
import time
import hashlib
import json
from dataclasses import asdict
from datetime import datetime


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
