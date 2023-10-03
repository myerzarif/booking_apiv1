from django.urls.conf import path
from .views import (
    TransactionView,
    ReservationView
)


app_name = "transaction"

urlpatterns = [
    path('', TransactionView.as_view(), name='search_transaction'),
    path('reservation', ReservationView.as_view(), name='create_reservation'),
]
