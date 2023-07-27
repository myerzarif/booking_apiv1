from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class MediumResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 300
