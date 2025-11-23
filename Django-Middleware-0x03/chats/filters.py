import django_filters
from chats.models import Message # Assuming Message model is importable

class MessageFilter(django_filters.FilterSet):
    """
    Allows filtering of Message objects by sender (user) and by time range.
    """
    # Filter by sender username (assuming User model has 'username')
    # Use __exact for exact match, or __icontains for partial/case-insensitive search
    sender__username = django_filters.CharFilter(
        field_name='sender__username', 
        lookup_expr='exact'
    )
    
    # Filter by date/time range: messages sent after this time
    created_after = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='gte', # Greater than or equal to
        label='Messages created after (YYYY-MM-DD HH:MM:SS)'
    )
    
    # Filter by date/time range: messages sent before this time
    created_before = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='lte', # Less than or equal to
        label='Messages created before (YYYY-MM-DD HH:MM:SS)'
    )

    class Meta:
        model = Message
        # You can add more fields from the model here
        fields = ['sender', 'sender__username', 'created_after', 'created_before']