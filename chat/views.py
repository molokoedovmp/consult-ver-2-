from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def chat_view(request, username):
    recipient = get_object_or_404(User, username=username)
    return render(request, 'chat/chat.html', {'recipient': recipient})
