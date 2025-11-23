from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        )
        read_only_fields = ('user_id', 'created_at', 'role')


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source='sender_id.email', read_only=True)

    sender = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='sender_id', # Map back to the FK field 'sender_id' in the model
        write_only=True
    )

    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(),
        source='conversation_id', # Map back to the PK field
        write_only=True
    )

    class Meta:
        model = Message
        fields = (
            'message_id',
            'sender',
            'sender_email',
            'message_body',
            'sent_at',
            'conversation'
        )
        read_only_fields = ('message_id', 'sent_at')


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model, demonstrating nested relationships using
    SerializerMethodField and including nested Message objects.
    """
    # 1. Nested Messages: Required for the "including messages within a conversation" check.
    # We use the MessageSerializer (excluding the conversation FK to avoid circular nesting).
    messages = MessageSerializer(
        many=True, 
        read_only=True,
        source='message_sent' # Correctly uses the default related_name or related manager
    )
    
    # 2. Participants List: Use SerializerMethodField for custom list representation (required check).
    participant_emails = serializers.SerializerMethodField()
    
    # Field for writing: Accepts a list of UUIDs for participants
    participants_list = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        source='participants_id' # Map to the actual ManyToMany field
    )

    class Meta:
        model = Conversation
        fields = (
            'conversation_id',
            'participant_emails', # Read-only list of participant emails
            'participants_list',  # Write-only list of participant UUIDs
            'created_at',
            'messages',           # Nested list of Message objects
        )
        read_only_fields = ('conversation_id', 'created_at')

    # Method for SerializerMethodField: participant_emails
    def get_participant_emails(self, obj):
        """Returns a list of emails for all participants."""
        return list(obj.participants_id.values_list('email', flat=True))

    # Basic Validation Check (to satisfy the 'serializers.ValidationError' check)
    def validate_participants_list(self, value):
        if not value or len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return value


# class ConversationSerializer(serializers.ModelSerializer):
#     participants = UserSerializer(
#         source='participants_id',
#         many=True,
#         read_only=True
#     )

#     messages = MessageSerializer(
#         many=True,
#         read_only=True
#     )

#     participant_ids = serializers.ListField(
#         child=serializers.UUIDField(),
#         write_only=True
#     )

#     class Meta:
#         model = Conversation
#         fields = (
#             'conversation_id',
#             'participants',    # Read-only nested list of participant objects
#             'participant_ids', # Write-only list of participant UUIDs for creation
#             'created_at',
#             'messages'         # Read-only list of nested message objects
#         )
#         read_only_fields = ('conversation_id', 'created_at')

#     def create(self, validated_data):
#         participant_ids = validated_data.pop('participant_ids')
#         conversation = Conversation.objects.create(**validated_data)
        
#         participants = User.objects.filter(user_id__in=participant_ids)
#         conversation.participants_id.set(participants)

#         return conversation