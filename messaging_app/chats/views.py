from rest_framework import viewsets
from rest_framework.permissions import AllowAny # Use IsAuthenticated for a real project
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer # Assuming UserSerializer exists

# Note: For a real-world application, you would enforce authentication here.
# We'll use AllowAny for initial project setup.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    We include this for testing purposes, assuming User creation/management.
    """
    queryset = User.objects.all().order_by('email')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    permission_classes = [AllowAny]

    # Optional: Customize queryset to only show conversations the current user is a part of
    # def get_queryset(self):
    #     user = self.request.user
    #     return Conversation.objects.filter(participants_id=user).order_by('-created_at')


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('sent_at')
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        queryset = Message.objects.all().order_by('sent_at')

        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)

        return queryset