from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            user=instance.receiver
        )
        notification.message.set([instance])