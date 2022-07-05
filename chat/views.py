from django.shortcuts import render

from chat.models import Message
from room.models import Room


def chat_room(request, room_id):
    room = Room.objects.get(id=room_id)
    messages = Message.objects.filter(room=room)[0:30]
    context = {'room': room, 'messages': messages}
    return render(request, 'chat/chat-room.html', context)
