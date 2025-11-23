from rest_framework import permissions
from .models import Conversation


class IsParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation 
    or message to view or edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request authenticated 
        # (covered by IsAuthenticated in REST_FRAMEWORK settings),
        # so we'll enforce object-level checks primarily for safe methods 
        # like GET, HEAD, OPTIONS, and all methods for security.

        user = request.user

        # 1. Check for Conversation (assuming 'obj' is a Conversation instance)
        if hasattr(obj, 'participants'):
            return obj.participants.filter(id=user.id).exists()
        
        # 2. Check for Message (assuming 'obj' is a Message instance)
        # Assuming the Message model has 'sender' and 'conversation' foreign keys
        elif hasattr(obj, 'sender'):
            # The sender can access their message
            if obj.sender == user:
                return True
            # Or, check if the user is a participant of the parent conversation
            elif hasattr(obj, 'conversation') and obj.conversation.participants.filter(id=user.id).exists():
                return True
        
        # Deny access if user is not a participant/sender
        return False
    

# messaging_app/chats/permissions.py


# class IsParticipantOfConversation(permissions.BasePermission):
#     """
#     Allows only authenticated users who are participants in a conversation 
#     to view, send, update, and delete related objects (Conversations and Messages).
#     """
    
#     # The has_permission method is implicitly handled by the global 
#     # 'IsAuthenticated' set in settings.py, but we keep the logic 
#     # specific to the object here.
    
#     def has_object_permission(self, request, view, obj):
#         user = request.user

#         # 1. Check if the object is a Conversation
#         if isinstance(obj, Conversation):
#             # Check if the user is a participant in this specific conversation instance
#             return obj.participants.filter(id=user.id).exists()
        
#         # 2. Check if the object is a Message
#         # The Message object is tied to a Conversation
#         # Assumes the Message model has a foreign key to Conversation called 'conversation'
#         elif hasattr(obj, 'conversation'):
#             # Check if the user is a participant of the parent conversation
#             return obj.conversation.participants.filter(id=user.id).exists()
        
#         # Default denial for safety if the object type is not recognized
#         return False

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows only authenticated users who are participants in a conversation 
    to view, send, update, and delete related objects.
    """
    
    # Check 1: Ensure only authenticated users can use the API
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated
    
    # Check 2: Restrict object-level access (PUT, PATCH, DELETE) to participants
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Check if the user is a participant. This core check applies to all methods.
        is_participant = False

        # 1. Check if the object is a Conversation
        if isinstance(obj, Conversation):
            is_participant = obj.participants.filter(id=user.id).exists()
        
        # 2. Check if the object is a Message
        elif hasattr(obj, 'conversation'):
            is_participant = obj.conversation.participants.filter(id=user.id).exists()
        
        # Explicitly check for unsafe methods, which are methods that modify data
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            # If it's a modifying method, the user MUST be a participant.
            return is_participant
            
        # For safe methods (GET, HEAD, OPTIONS), the user must also be a participant
        # based on the objective "Allow only participants... to view... messages"
        return is_participant