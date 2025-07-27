from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from .permissions import IsParticipantOfConversation, IsOwnerOrParticipant
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from .pagination import MessagePagination
from .filters import MessageFilter
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_403_FORBIDDEN

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrParticipant]

    def get_queryset(self):
        # List only conversations the current user is part of
        return Conversation.objects.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically add the current user as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
            return Response({'status': 'participant added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrParticipant]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        conversation = get_object_or_404(Conversation, pk=conversation_id)

    if request.user not in conversation.participants.all():
        raise PermissionDenied(detail="You are not a participant in this conversation.", code=HTTP_403_FORBIDDEN)


        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)