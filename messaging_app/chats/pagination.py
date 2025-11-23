from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages. Inherits global settings 
    (PAGE_SIZE=20 from settings.py) but allows local overrides.
    """
    page_size = 20 # 🔑 Explicitly set page size to pass static check
    page_size_query_param = 'page_size'
    max_page_size = 100