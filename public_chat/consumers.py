

import json
from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
from django.utils import timezone

from public_chat.models import PublicChatRoom, PublicChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept',
        })
        # await asyncio.sleep(5)

        room = await self.get_room()
        self.room = room
        chat_room = room.title
        self.chat_room = chat_room

        await self.connect_user(room)

        # Join room group
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )



    async def websocket_disconnect(self, event):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )

    async def websocket_receive(self, event):
        # when the message is received from the websocket
        print('receive: ', event)
        # receive {'type': 'websocket.receive', 'text': '{"message":"aaa23"}'}
        front_text = event.get("text", None)
        if front_text is not None:
            dict_data = json.loads(front_text)
            message = dict_data['message']

            message_object = await self.create_new_chat_message(message)
            message_object_id = message_object.pk
            my_response = {
                'message': message,
                'user': self.scope['user'].username,
                'user_id': self.scope['user'].pk,
                'profile_image': str(self.scope['user'].profile_image.url),
                'timestamp': str(timezone.now()),
                'message_id': message_object_id,
            }

            # broadcasts the message event to be send
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(my_response),
                }
            )

    @database_sync_to_async
    def connect_user(self, room):
        room.connect_user(self.scope['user'])

    @database_sync_to_async
    def create_new_chat_message(self, message):
        msg = PublicChatMessage.objects.create(
            user=self.scope['user'],
            room=self.room,
            content=message)
        return msg

    @database_sync_to_async
    def get_room(self):
        try:
            room = PublicChatRoom.objects.get(title='room1')
        except Exception:
            room = PublicChatRoom.objects.create(
                title='room1')
            room.users.add(self.scope['user'])
        return room

    async def chat_message(self, event):
        # send the actual message


        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })