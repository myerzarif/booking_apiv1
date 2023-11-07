from datetime import datetime, date, timedelta
import django_filters
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    date_duration = django_filters.CharFilter(
        field_name='created_at', method='created_days')
    
    created_at_from = django_filters.DateTimeFilter(field_name='created_at', method='created_at_from_filter')
    created_at_to = django_filters.DateTimeFilter(field_name='created_at', method='created_at_to_filter')

    def created_at_from_filter(self, queryset, name, value):
        return queryset.filter(created_at__gte=value)
    
    def created_at_to_filter(self, queryset, name, value):
        return queryset.filter(created_at__lte=value)
    
    def created_days(self, queryset, name, value):
        today = datetime.now()
        if value == "Today":
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            return queryset.filter(created_at__gte=start_date, created_at__lte=end_date)
        elif value == "Yesterday":
            start_date = (today - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            return queryset.filter(created_at__gte=start_date, created_at__lte=end_date)
        elif value == "This Week":
            start_date = (today - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = today
            return queryset.filter(created_at__gte=start_date, created_at__lte=end_date)
        elif value == "Last Week":
            start_date = (today - timedelta(days=13)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = (today - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
            return queryset.filter(created_at__gte=start_date, created_at__lte=end_date)
        elif value == "This Month":
            start_date = (today.replace(day=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = today
            return queryset.filter(created_at__gte=start_date, created_at__lte=end_date)
        elif value == "Last Month":
            start_date = (today.replace(day=1)-timedelta(days=1)).replace(day=1).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = (today.replace(day=1)-timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)
            return queryset.filter(created_at__gte=start_date, created_at__lte=end_date)
        elif value == "All Time":
            return queryset

    class Meta:
        model = Transaction
        fields = ["status",
                  "date_duration",
                  "created_at",
                  "created_at_from",
                  "created_at_to",
                  ]
