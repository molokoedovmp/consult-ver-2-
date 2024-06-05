from django.urls import path
from .views import chat, chat_list

urlpatterns = [
    path('chats/', chat_list, name='chat_list'),
    path('chat/<str:email>/', chat, name='chat'),
]
