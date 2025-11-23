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
    sender = UserSerializer(read_only=True)

    sender_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = (
            'message_id',
            'sender',
            'sender_id',
            'message_body',
            'sent_at',
            'conversation_id'
        )
        read_only_fields = ('message_id', 'sent_at')



class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(
        source='participants_id',
        many=True,
        read_only=True
    )

    messages = MessageSerializer(
        many=True,
        read_only=True
    )

    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )

    class Meta:
        model = Conversation
        fields = (
            'conversation_id',
            'participants',    # Read-only nested list of participant objects
            'participant_ids', # Write-only list of participant UUIDs for creation
            'created_at',
            'messages'         # Read-only list of nested message objects
        )
        read_only_fields = ('conversation_id', 'created_at')

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create(**validated_data)
        
        participants = User.objects.filter(user_id__in=participant_ids)
        conversation.participants_id.set(participants)

        return conversation