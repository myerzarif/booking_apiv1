import django_filters
from .models import User
from django.db.models import Q


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_by_name')
    email = django_filters.CharFilter(lookup_expr='icontains')
    mobile = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = {
            'role': ['exact'],
        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )
