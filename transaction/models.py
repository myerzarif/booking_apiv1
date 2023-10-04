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
    hotel_amount = models.DecimalField(max_digits=7, decimal_places=2)
    car_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    hotel_fee_amount = models.DecimalField(max_digits=7, decimal_places=2)
    car_fee_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)

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
    payer = models.CharField(max_length=200, blank=True, null=True)

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
