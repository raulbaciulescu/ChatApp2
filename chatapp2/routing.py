from public_chat.consumers import ChatConsumer
from django.urls import re_path, path

websocket_urlpatterns = [
    # re_path(r'messages/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'', ChatConsumer.as_asgi()),
    #path('', ChatConsumer.as_asgi()),
]