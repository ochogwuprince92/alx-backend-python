from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

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
@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    print(f"User {instance.username} deleted. Cleaning up related data.")
    # If you're not using on_delete=CASCADE, you could manually delete here:
    # Message.objects.filter(sender=instance).delete()
    # Message.objects.filter(receiver=instance).delete()
    # Notification.objects.filter(user=instance).delete()
    # MessageHistory.objects.filter(message__sender=instance).delete()