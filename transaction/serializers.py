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
import stripe
import logging

logger = logging.getLogger('project.transaction')


class TransactionSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')
    reservation = serializers.SerializerMethodField('get_reservation')

    class Meta:
        model = Transaction
        fields = [
            "id",
            "created_at",
            "user",
            "status",
            "comment",
            "reservation"
        ]
        read_only_fields = ['id']

    def get_user(self, instance):
        return UserSerializer(User.objects.get(pk=instance.user_id)).data

    def get_reservation(self, instance):
        return ReservationDetailSerializer(Reservation.objects.get(pk=instance.reservation_id)).data

class PaymentSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "reservation",
            "first_name",
            "last_name",
            "country",
            "mobile",
        ]
        read_only_fields = ['id']

    def initiate_payment(self, data, user):
        reservation_data = Reservation.objects.get(pk=data.get("reservation")).to_dict()
        print("datadatadatadatadata", data)
        print("reservation_datareservation_datareservation_data", reservation_data)
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            intent = stripe.PaymentIntent.create(
                amount=int(to_decimal(reservation_data.get("total_amount")) * 100),
                currency='usd',
                receipt_email=user.email
            )
            print("intent_intent_intent_intent", intent)
            return intent.get('client_secret')
        except Exception as e:
            logger.error("payment intent creation error. {}".format(str(e)))
            raise exceptions.ValidationError("Payment validation error!")

class StripeWebhookSerializer(serializers.Serializer):
    pass

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     payload = request.get_data()
#     sig_header = request.headers.get('Stripe_Signature', None)

#     if not sig_header:
#         return 'No Signature Header!', 400

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return 'Invalid payload', 400
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return 'Invalid signature', 400

#     if event['type'] == 'payment_intent.succeeded':
#         email = event['data']['object']['receipt_email'] # contains the email that will recive the recipt for the payment (users email usually)
        
#         user_info['paid_50'] = True
#         user_info['email'] = email
#     else:
#         return 'Unexpected event type', 400

#     return '', 200

class HolderSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)


class ReservationSerializer(serializers.Serializer):
    item_id = serializers.CharField(required=True)
    car_code = serializers.CharField(required=False, allow_blank=True)

    def initiate_reservation(self, hotel_item, rental_car, user):
        days = hotel_item.get("search_params").get("days")
        hotel_amount = to_decimal(hotel_item.get("rate", {}).get("hotel_rate"))
        hotel_fee_amount = to_decimal(hotel_item.get("rate", {}).get(
            "hotel_rate") * settings.HOTEL_FEE_PERCENTAGE/100)
        total_hotel_amount = to_decimal(hotel_amount + hotel_fee_amount)

        car_amount = to_decimal(rental_car.get("price", 0) * days)
        car_fee_amount = to_decimal(rental_car.get("price", 0) * days * settings.CAR_FEE_PERCENTAGE/100)
        total_car_amount = to_decimal(car_amount + car_fee_amount)

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
            "total_hotel_amount": total_hotel_amount,
            "total_car_amount": total_car_amount,
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
            raise exceptions.ValidationError(
                "Hotel is not valid! Please try to search again.")

        rental_car = HbRental().get_doc_by_code(self.validated_data.get(
            "car_code")) if self.validated_data.get("car_code") else {}

        return self.initiate_reservation(hotel_item, rental_car, user)


class ReservationDetailSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
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
            "total_hotel_amount",
            "total_car_amount",
            "hotel_amount",
            "car_amount",
            "hotel_fee_amount",
            "car_fee_amount"
        ]
        read_only_fields = ['id']
