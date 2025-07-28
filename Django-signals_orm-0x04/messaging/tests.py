from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='password')
        self.receiver = User.objects.create_user(username='bob', password='password')

    def test_message_creation(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello!'
        )
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.content, 'Hello!')

    def test_notification_creation_and_linking(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Test notification'
        )
        notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notifications.count(), 1)

        notification = notifications.first()
        self.assertIn(message, notification.message.all())
