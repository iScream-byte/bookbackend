import sys
from rest_framework.pagination import PageNumberPagination
from django.conf import settings

from rest_framework.response import Response


class MyPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })