# chats/permissions.py

from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assuming 'participants' is a list of users in the conversation
        return request.user in obj.participants.all()
        
class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only participants of a conversation can access and modify it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For Conversation objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # For Message objects (accessed through their conversation)
        if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            is_participant = request.user in obj.conversation.participants.all()

            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return is_participant  # Only participants can modify/delete
            return is_participant  # Also restrict read/view/send to participants

        return False
