from dataclasses import dataclass


class HttpMethods:
    GET = "GET"
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'
    OPTION = 'OPTION'


class ContentTypes:
    FORM = "multipart/form-data"
    JSON = "application/json"
    XML = "application/xml"


class UserType:
    email = "email"
    mobile = "mobile"
    uuid = "uuid"


@dataclass
class Coordinates:
    longitude: float
    latitude: float


@dataclass
class Address:
    content: str
    street: str
    number: str


@dataclass
class Phone:
    number: str
    type: str
