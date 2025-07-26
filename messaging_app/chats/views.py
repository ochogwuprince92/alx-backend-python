from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from .permissions import IsOwnerOrParticipant. isParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_frmework.exceptions import Permission_denied
from .pagination import MessagePagination
from .filters import MessageFilter

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrParticipant]

    def get_queryset(self):
        # List only conversations the current user is part of
        return Conversation.objects.filter(participants=self.request.user)
    
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Automatically add the current user as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response({'status': 'participant added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrParticipant]
    pagination_class = MessagePagination
    filter_backends = (DjangoFilterBackend)
    filterset_class = MessageFilter

    def get_queryset(self):
        # Show messages only from conversations the user is part of
        return Message.objects.filter(sender=self.request.user)
        return self.queryset.filter(conversation__participants=self.request.user)
    
    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        conversation = Conversation.objects.get(id=conversation_id)

        if request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        return super().create(request, *args, **kwargs)