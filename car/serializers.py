
from django_restql.mixins import DynamicFieldsMixin
from car.base.models import CarData
from rest_framework_dataclasses.serializers import DataclassSerializer
from rest_framework import serializers
from typing import Literal, Optional
from common.extensions import mongo_default_db
from common.utils import generate_unique_id
from datetime import datetime


class CarSerializer(serializers.Serializer):
    """
    Serializer for Hotel Content View
    get a code and return the hotel data (some fields like [rooms, images, facilities] can be excluded in response)
    """

    name = serializers.CharField()
    type = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.FloatField()
    active = serializers.BooleanField()
    image = serializers.CharField()

    def create(self, model):
        model["code"] = generate_unique_id()
        model["created_at"] = datetime.utcnow()
        mongo_default_db["rental_car"].insert_one(model)


class CarRentalSerializer(DataclassSerializer):
    """
    Serializer for Car Content View
    get a code and return the car data
    """

    class Meta:
        dataclass = CarData


class CarQueryParamSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
