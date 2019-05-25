from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultResultSetPagination(PageNumberPagination):
    """
    Override default paginator class
    """

    page_size = 12

    def get_paginated_data(self, data):
        return {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        }

    def get_paginated_response(self, data):
        return Response(self.get_paginated_data(data))
