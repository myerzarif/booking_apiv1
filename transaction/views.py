from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from config.logger import LoggerMixin
from transaction.serializers import TransactionSerializer, ReservationSerializer
from rest_framework import generics, exceptions, permissions
from rest_framework.generics import ListAPIView, CreateAPIView
from common.pagination import MediumResultsSetPagination
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filter
from .filters import TransactionFilter
from .models import Transaction, Reservation
from rest_framework.serializers import Serializer
from .serializers import UserDetailSerializer


class TransactionView(LoggerMixin, ListAPIView):
    """
    List Transaction
    """
    serializer_class = TransactionSerializer
    pagination_class = MediumResultsSetPagination
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filter.SearchFilter, rest_filter.OrderingFilter]
    filter_class = TransactionFilter
    permission_classes = [IsAuthenticated]
    name = "transaction"
    ordering_fields = ('payer', 'user', 'status', 'created_at', "total_amount")
    ordering = ('-created_at')

    def get_queryset(self):
        return Transaction.objects.all().filter(active=True)


class ReservationView(LoggerMixin, generics.GenericAPIView):
    """
    Initiate a Reservation
    """
    permission_classes = []
    serializer_class = ReservationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # params = serializer.validated_data
        result = serializer.reserve(request.user)
        return Response(data=result, status=200)


class ReservationDetailView(LoggerMixin, generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        return Reservation.objects.filter(active=True)