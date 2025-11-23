from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer # Assuming UserSerializer exists
from .permissions import IsParticipant, IsParticipantOfConversation


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('email')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# class ConversationViewSet(viewsets.ModelViewSet):
#     queryset = Conversation.objects.all().order_by('-created_at')
#     serializer_class = ConversationSerializer
#     permission_classes = [AllowAny]


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    # 🔑 Apply the custom permission here
    permission_classes = [IsAuthenticated, IsParticipant, IsParticipantOfConversation]
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    
    # Add filters backend
    filter_backends = [DjangoFilterBackend]
    # Define fields available for filtering (e.g., filter by created_at)
    filterset_fields = ['created_at']

    # Custom action to demonstrate use of 'status' and custom endpoint logic
    @action(detail=True, methods=['post'], name='archive')
    def archive(self, request, pk=None):
        """Allows archiving a conversation."""
        conversation = self.get_object()
        # Logic to archive the conversation would go here (e.g., setting a flag)
        # For demonstration, we just return a status response
        return Response({'status': f'Conversation {conversation.conversation_id} archived'}, 
                        status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('sent_at')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant, IsParticipantOfConversation]    
    # Add filters backend
    filter_backends = [DjangoFilterBackend]
    # Define fields available for filtering (e.g., filter by sender)
    filterset_fields = ['sender_id', 'conversation_id']

# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all().order_by('sent_at')
#     serializer_class = MessageSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         conversation_id = self.request.query_params.get('conversation_id')
#         queryset = Message.objects.all().order_by('sent_at')

#         if conversation_id:
#             queryset = queryset.filter(conversation__conversation_id=conversation_id)

#         return queryset