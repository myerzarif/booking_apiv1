from datetime import datetime, date, timedelta
import django_filters
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    date_duration = django_filters.CharFilter(
        field_name='created_at', method='created_days')

    def created_days(self, queryset, name, value):
        if value == "Today":
            start_date = date.today()
            end_date = date.today()
            return queryset.filter(created_at__gte=datetime.date(start_date),
                                   created_at__lte=datetime.date(end_date))
        elif value == "Yesterday":
            start_date = date.today() - timedelta(days=1)
            end_date = start_date - timedelta(days=1)
            return queryset.filter(created_at__gte=datetime.date(start_date),
                                   created_at__lte=datetime.date(end_date))
        elif value == "This Week":
            start_date = date.today() - timedelta(days=6)
            end_date = date.today()
            return queryset.filter(created_at__gte=datetime.date(start_date),
                                   created_at__lte=datetime.date(end_date))
        elif value == "Last Week":
            start_date = date.today() - timedelta(days=13)
            end_date = date.today() - timedelta(days=7)
            return queryset.filter(created_at__gte=datetime.date(start_date),
                                   created_at__lte=datetime.date(end_date))
        elif value == "This Month":
            start_date = date.today().replace(day=1)
            end_date = date.today()
            return queryset.filter(created_at__gte=datetime.date(start_date),
                                   created_at__lte=datetime.date(end_date))
        elif value == "Last Month":
            start_date = date.today().replace(day=1) - timedelta(month=1)
            end_date = start_date + timedelta(month=1) - timedelta(days=1)
            return queryset.filter(created_at__gte=datetime.date(start_date),
                                   created_at__lte=datetime.date(end_date))
        elif value == "All Time":
            return queryset

    class Meta:
        model = Transaction
        fields = ["payer",
                  "status",
                  "date_duration",
                  "created_at"]
