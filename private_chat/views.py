from django.shortcuts import render

# Create your views here.

def chat_view(request, *args, **kwargs):
    context = {
        'user1': kwargs.get('user1'),
        'user2': kwargs.get('user2'),
    }
    return render(request, 'private_chat/chat.html', context)
