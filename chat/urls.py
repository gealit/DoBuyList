from django.urls import path

from chat.views import chat_room

urlpatterns = [
    path('chat/<int:room_id>/', chat_room, name='chat')
]
