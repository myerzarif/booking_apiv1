"""validator for Account App"""
import re
from rest_framework import exceptions

def password_validator(value):
    """
    Password Validator by Regex
    if wrong raise exception
    return None
    """
    password_pattern = re.compile(r'^[a-zA-Z0-9@!\#\-\\ \_\$\%\^\*\&\(\)]{8,140}$')
    if not password_pattern.match(value):
        raise exceptions.ValidationError("Password length must be at least 8 characters and consists of english alphanumerics!")


def email_validator(value):
    """
    Email Validator by Regex
    if wrong raise exception
    return None
    """
    email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if not email_pattern.match(value):
        raise exceptions.ValidationError("Email format is not correct!")


def confirm_password_validator(params):
    """
    Check id confirm password is the same as password
    """
    if params.get("password") != params.get("confirm_password"):
        raise exceptions.ValidationError(detail="Password and confirm password fields are not the same!")


def address_validator(value):
    """
    Address Validator - Check the length of the address
    """
    address_pattern = re.compile(r'^[a-zA-Z0-9@!\#\-\_\\ \$\%\^\*\&\(\)]{10,1000}$')
    if not address_pattern.match(value):
        raise exceptions.ValidationError("Adddress length must be at least 10 characters and consists of english alphanumerics!")
