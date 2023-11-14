from django.urls.conf import path
from .views import (
    TransactionView,
    ReservationView,
    ReservationDetailView,
    PaymentView,
    StripeWebhookView,
    TransactionDetailView
)


app_name = "transaction"

urlpatterns = [
    path('', TransactionView.as_view(), name='search_transaction'),
    path('reservation', ReservationView.as_view(), name='create_reservation'),
    path('<str:pk>', TransactionDetailView.as_view(), name='detail_transaction'),
    path('reservation/<str:pk>', ReservationDetailView.as_view(), name='detail_reservation'),
    path('payment', PaymentView.as_view(), name='create_payment'),
    path('stripe/webhook', StripeWebhookView.as_view(), name='stripe_webhook'),
]
