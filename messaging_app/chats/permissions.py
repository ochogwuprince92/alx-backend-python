# chats/permissions.py

from rest_framework.permissions import BasePermission

class IsOwnerOrParticipant(BasePermission):
    """
    Custom permission to only allow users to access their own messages or conversations.
    """

    def has_object_permission(self, request, view, obj):
        # Assumes `obj` has a `sender` or `participants` attribute
        return request.user == obj.sender or request.user in obj.participants.all()
