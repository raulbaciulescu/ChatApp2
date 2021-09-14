
from private_chat.consumers import PrivateChatConsumer
from public_chat.consumers import ChatConsumer
from django.urls import re_path, path

websocket_urlpatterns = [
    path('chat/<user1>_<user2>/', PrivateChatConsumer.as_asgi()),
    re_path(r'', ChatConsumer.as_asgi()),
    #re_path(r'', NotificationConsumer.as_asgi()),
    # path('', ChatConsumer.as_asgi()),
    #re_path(r'chat/(?P<user1_user2>\w+)/$', PrivateChatConsumer.as_asgi()),
    #path('chat/<username>/', PrivateChatConsumer.as_asgi()),
]