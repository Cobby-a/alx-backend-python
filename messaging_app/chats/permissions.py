from rest_framework import permissions

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