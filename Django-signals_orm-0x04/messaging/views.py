from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Message, Notification

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # log out the user first
    user.delete()    # trigger post_delete signal
    return redirect('home')  # redirect to home or goodbye page

@login_required    
def user_messages(request):
    # Step 1: Filter messages where sender is the logged-in user
    messages = Message.objects.filter(sender=request.user)\
        .select_related('receiver')\
        .prefetch_related('replies', 'replies__sender')

    return render(request, 'messaging/user_messages.html', {'messages': messages})

@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user)

    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_messages
    })

# Fetch top-level messages in a conversation with replies
messages = Message.objects.filter(parent_message__isnull=True).select_related('sender', 'receiver').prefetch_related('replies')

def get_threaded_messages(message):
    """
    Recursively get all replies for a given message
    """
    thread = []
    for reply in message.replies.all():
        thread.append({
            'id': reply.id,
            'sender': reply.sender.username,
            'content': reply.content,
            'timestamp': reply.timestamp,
            'replies': get_threaded_messages(reply)
        })
    return thread

top_messages = Message.objects.filter(parent_message__isnull=True).prefetch_related('replies', 'replies__sender', 'replies__replies')

for msg in top_messages:
    print(f"{msg.sender.username}: {msg.content}")
    replies = get_threaded_messages(msg)
    print(replies)

def inbox(request):
    user = request.user
    unread_messages = Message.unread.for_user(user)
    ...
