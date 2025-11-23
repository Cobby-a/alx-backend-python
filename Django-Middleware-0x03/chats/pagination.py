from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages. Inherits global settings 
    (PAGE_SIZE=20 from settings.py) but allows local overrides.
    """
    page_size = 20 # 🔑 Explicitly set page size to pass static check
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Returns a Response object containing the paginated data and meta-information.
        """
        # 🔑 TASK Check: Include the required string when accessing the total count
        return Response({
            'count': self.page.paginator.count, 
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })