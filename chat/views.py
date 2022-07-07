from django.http import Http404
from django.shortcuts import render

from chat.models import Message
from room.models import Room


def chat_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if not request.user in room.participants.all():
        raise Http404
    messages = Message.objects.filter(room=room)[0:30].select_related('room').select_related('user')
    context = {'room': room, 'messages': messages}
    return render(request, 'chat/chat-room.html', context)
