from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin
from .models import Transaction
from account.models import User
from account.serializers import UserSerializer
from hotel.base.availability import Availability
from hotel.hotelbeds.availability import HbAvailability
from car.base.rental import Rental
from car.hotelbeds.rental import HbRental
from common.utils import generate_unique_id, to_decimal
from .models import Reservation
from rest_framework import exceptions

class TransactionSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Transaction
        fields = [
            "id",
            "created_at",
            "user",
            "payer",
            "status",
            "comment",
        ]
        read_only_fields = ['id']

    def get_user(self, instance):
        return UserSerializer(User.objects.get(pk=instance.user_id)).data

# {
# 	id: "54e40663-93e0-4a2a-9d2b-04c1001d1ec2",
# 	room_code: "DBL.DX",
# 	rate_key: "20231010|20231011|W|148|88930|DBL.DX|FIT..",
# 	bank_account: {},
# 	holder_info: {}
# }


class HolderSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)


class ReservationSerializer(serializers.Serializer):
    item_id = serializers.CharField(required=True)
    car_code = serializers.CharField(required=False, allow_blank=True)

    def initiate_reservation(self, hotel_item, rental_car, user):
        hotel_amount = to_decimal(hotel_item.get("rate", {}).get("hotel_rate"))
        car_amount = to_decimal(rental_car.get("price", 0))
        hotel_fee_amount = to_decimal(hotel_item.get("rate", {}).get(
            "hotel_rate") * settings.HOTEL_FEE_PERCENTAGE/100)
        car_fee_amount = to_decimal(rental_car.get(
            "price", 0) * settings.CAR_FEE_PERCENTAGE/100)
        total_amount = to_decimal(
            hotel_amount + car_amount + hotel_fee_amount + car_fee_amount)

        reservation_doc = {
            "reference_id": generate_unique_id(),
            "user": user if not user.is_anonymous else None,
            "hotel_code": hotel_item.get("hotel", {}).get("code"),
            "hotel_name": hotel_item.get("hotel", {}).get("name"),
            "room_code": hotel_item.get("room", {}).get("code"),
            "room_description": hotel_item.get("room", {}).get("description"),
            "rate_key": hotel_item.get("rate", {}).get("rate_key"),
            "hotel_item_id": hotel_item.get("item_id"),
            "car_code": rental_car.get("code"),
            "car_name": rental_car.get("name"),
            "search": hotel_item.get("search_params"),
            "total_amount": total_amount,
            "hotel_amount": hotel_amount,
            "car_amount": car_amount,
            "hotel_fee_amount": hotel_fee_amount,
            "car_fee_amount": car_fee_amount
        }

        reservation = Reservation(**reservation_doc)
        reservation.save()
        reservation_doc["reservation_id"] = str(reservation.id)
        return reservation_doc

    def reserve(self, user):
        hotel_item = HbAvailability().get_doc_by_item_id(
            self.validated_data.get("item_id"))
        
        if not hotel_item:
            raise exceptions.ValidationError("Hotel is not valid! Please try to search again.")
        
        rental_car = HbRental().get_doc_by_code(self.validated_data.get(
            "car_code")) if self.validated_data.get("car_code") else {}

        return self.initiate_reservation(hotel_item, rental_car, user)


class UserDetailSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """Serializer For Reservation Model"""

    class Meta:
        model = Reservation
        fields = [
            "id",
            "reference_id",
            "user",
            "hotel_code",
            "hotel_name",
            "room_code",
            "room_description",
            "rate_key",
            "hotel_item_id",
            "car_code",
            "car_name",
            "search",
            "total_amount",
            "hotel_amount",
            "car_amount",
            "hotel_fee_amount",
            "car_fee_amount"
        ]
        read_only_fields = ['id']
