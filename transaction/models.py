from io import BytesIO
from django.core.files.storage import default_storage
from django.db import models
from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions
from secrets import token_urlsafe
import logging
import uuid
from django.utils.translation import gettext_lazy
from common.models import BaseModel

logger = logging.getLogger("project.transaction")


class Reservation(BaseModel):
    class ReservationStatus(models.TextChoices):
        INITIATE = 'Initiate', gettext_lazy('INITIATE')
        DONE = 'DONE', gettext_lazy('DONE')

    reference_id = models.TextField(max_length=32)
    user = models.ForeignKey(
        "account.User", on_delete=models.PROTECT, blank=True, null=True)

    hotel_code = models.IntegerField()
    hotel_name = models.TextField()
    room_code = models.TextField()
    room_description = models.TextField()
    rate_key = models.TextField()
    hotel_item_id = models.TextField()
    car_code = models.TextField(blank=True, null=True)
    car_name = models.TextField(blank=True, null=True)
    search = models.JSONField()

    total_amount = models.DecimalField(max_digits=7, decimal_places=2)
    total_hotel_amount = models.DecimalField(max_digits=7, decimal_places=2)
    total_car_amount = models.DecimalField(max_digits=7, decimal_places=2)
    hotel_amount = models.DecimalField(max_digits=7, decimal_places=2)
    car_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    hotel_fee_amount = models.DecimalField(max_digits=7, decimal_places=2)
    car_fee_amount = models.DecimalField(
        max_digits=7, decimal_places=2, null=True)

    status = models.CharField(
        max_length=15,
        choices=ReservationStatus.choices,
        default=ReservationStatus.INITIATE,
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["-created_at"]

    def to_dict(self):
        return {
            "reservation_id": str(self.id),
            "reference_id": str(self.id),
            "user": None,
            "hotel_code": self.hotel_code,
            "hotel_name": self.hotel_name,
            "room_code": self.room_code,
            "room_description": self.room_description,
            "rate_key": self.rate_key,
            "hotel_item_id": self.hotel_item_id,
            "car_code": self.car_code,
            "car_name": self.car_name,
            "search": self.search,
            "total_amount": self.total_amount,
            "total_hotel_amount": self.total_hotel_amount,
            "total_car_amount": self.total_car_amount,
            "hotel_amount": self.hotel_amount,
            "car_amount": self.car_amount,
            "hotel_fee_amount": self.hotel_fee_amount,
            "car_fee_amount": self.car_fee_amount
        }


class Transaction(BaseModel):
    class TransactionStatus(models.TextChoices):
        INITIATE = 'Initiate', gettext_lazy('INITIATE')
        PAID = 'Paid', gettext_lazy('PAID')
        SUCCESS = 'Success', gettext_lazy('SUCCESS')
        FAILED = 'Failed', gettext_lazy('FAILED')
        CANCELLED = 'Cancelled', gettext_lazy('CANCELLED')
        REFUND = 'Refund', gettext_lazy('REFUND')

    user = models.ForeignKey("account.User", on_delete=models.PROTECT)
    reservation = models.ForeignKey(
        "transaction.Reservation", on_delete=models.PROTECT)
    currency = models.TextField(max_length=3, blank=True, null=True)
    payment_method = models.TextField(max_length=10, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    intent_client_secret = models.TextField(blank=True, null=True)

    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)

    status = models.CharField(
        max_length=15,
        choices=TransactionStatus.choices,
        default=TransactionStatus.INITIATE,
    )

    def __str__(self):
        return self.id

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["-created_at"]
