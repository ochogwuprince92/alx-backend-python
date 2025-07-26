# chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to interact with it.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check for conversation participants
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        # Check for message objects
        if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            return request.user in obj.conversation.participants.all()
        return False
