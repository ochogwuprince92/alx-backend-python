from rest_framework import serializers
from .models import User, Conversation, Message

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'conversation', 'content', 'timestamp']

    # Validation example (using serializers.ValidationError)
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be empty.")
        return value

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'bio']

# Conversation Serializer (with SerializerMethodField)
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.all().order_by('timestamp')
        return MessageSerializer(messages, many=True).data
