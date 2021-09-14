
from django.shortcuts import render

def room(request, room_name):
    return render(request, 'public_chat/room.html', {
        'room_name': room_name,
        'user': request.user,
    })