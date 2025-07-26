# chats/permissions.py

from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to allow only owners or conversation participants to access the object.
    """

    def has_object_permission(self, request, view, obj):
        # For a Conversation object
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        # For a Message object
        if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            return request.user in obj.conversation.participants.all()
        return False
