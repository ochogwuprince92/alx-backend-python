from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            user=instance.receiver
        )
        notification.message.set([instance])

def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            instance.edited = True  # Set the edited flag
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content
            )