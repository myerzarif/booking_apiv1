"""validator for Account App"""
import re
from rest_framework import exceptions
from django.contrib.auth import password_validation

def password_validator(value):
    """
    Password Validator by Regex
    if wrong raise exception
    return None
    """
    password_pattern = re.compile(r'^[a-zA-Z0-9@!\#\-\\ \_\$\%\^\*\&\(\)]{5,140}$')
    if not password_pattern.match(value):
        raise exceptions.ValidationError("Password length must be at least 5 characters and consists of english alphanumerics!")
    # password_validation.validate_password(value)    
    try: 
        password_validation.validate_password(value)
    except exceptions.ValidationError as error:
            raise exceptions.ValidationError("The new password is not met password policies!")

def email_validator(value):
    """
    Email Validator by Regex
    if wrong raise exception
    return None
    """
    email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if not email_pattern.match(value):
        raise exceptions.ValidationError("Email format is not correct!")

def username_type(username):
    email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    phone_pattern = re.compile("^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$")
    uuid_pattern = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$")
    if email_pattern.match(username):
        return 'email'
    elif phone_pattern.match(username):
        return 'phone'
    elif uuid_pattern.match(username):
        return 'uuid'
    return 'None'
    
def confirm_password_validator(params):
    """
    Check id confirm password is the same as password
    """
    if params.get("password") != params.get("confirm_password"):
        raise exceptions.ValidationError("Password and confirm password fields are not the same!")


def address_validator(value):
    """
    Address Validator - Check the length of the address
    """
    address_pattern = re.compile(r'^[a-zA-Z0-9@!\#\-\_\\ \$\%\^\*\&\(\)]{10,1000}$')
    if not address_pattern.match(value):
        raise exceptions.ValidationError("Address length must be at least 10 characters and consists of english alphanumerics!")

def validate_email(loggedUser, email):
    if loggedUser != email:
        raise exceptions.ValidationError("You can not change password of other users!")
    
def validate_confirm(new_password, confirm_password):
    if confirm_password and new_password != confirm_password:
        raise exceptions.ValidationError("Please confirm new password correctly!")

class NumberValidator(object):
    def __init__(self, min_digits=1):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if not len(re.findall('\d', password)) >= self.min_digits:
            raise exceptions.ValidationError(
                "The password must contain at least {0} digit(s), 0-9.".format(self.min_digits),
                code='password_no_number',
            )

    def get_help_text(self):
        return "Your password must contain at least {0} digit(s), 0-9.".format(self.min_digits)


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise exceptions.ValidationError(
                "The password must contain at least 1 uppercase letter, A-Z.",
                code='password_no_upper',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 uppercase letter, A-Z."
    

class LowercaseValidator:
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise exceptions.ValidationError(
                "The password must contain at least 1 lowercase letter, a-z.",
                code='password_no_lower',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 lowercase letter, a-z."
    