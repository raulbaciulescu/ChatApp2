from django.urls import path

from private_chat.views import chat_view

app_name = 'private_chat'

urlpatterns = [
    path('<user1>_<user2>/', chat_view, name='private-chat'),
    #path('<username>/', chat_view, name='private-chat'),
]