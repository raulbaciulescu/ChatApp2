import json
from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core.paginator import Paginator
from django.core.serializers.base import Serializer
from django.utils import timezone

from account.models import Account
from private_chat.models import PrivateChat, PrivateMessage


class PrivateChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept',
        })
        user2 = self.scope['url_route']['kwargs']['user2']
        user1 = self.scope['url_route']['kwargs']['user1']
        chat = await self.get_chat_object(user1, user2)

        self.chat_obj = chat
        self.chat = f'chat{chat.pk}'  # chat name
        await self.channel_layer.group_add(
            self.chat,
            self.channel_name
        )

    async def websocket_receive(self, event):
        # when the message is received from the websocket
        print('receive private chat: ', event)
        front_text = event.get('text', None)

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
                self.chat,
                {
                    'type': 'chat_message',
                    'text': json.dumps(my_response),
                }
            )

    async def websocket_disconnect(self, event):
        # Leave chat
        await self.channel_layer.group_discard(
            self.chat,
            self.channel_name
        )

    @database_sync_to_async
    def get_chat_object(self, user1, user2):
        if user1 < user2:
            account1 = Account.objects.get(username=user1)
            account2 = Account.objects.get(username=user2)
        else:
            account1 = Account.objects.get(username=user2)
            account2 = Account.objects.get(username=user1)

        try:
            chat = PrivateChat.objects.get(first=account1, second=account2)
        except PrivateChat.DoesNotExist:
            chat = PrivateChat.objects.create(first=account1, second=account2)
        return chat

    @database_sync_to_async
    def create_new_chat_message(self, message):
        msg = PrivateMessage.objects.create(
            user=self.scope['user'],
            chat=self.chat_obj,
            content=message)
        return msg

    # @database_sync_to_async
    # def get_chat_messages(self, chat, page_number):
    #     try:
    #         messages = PrivateMessage.objects.filter(chat=chat).order_by('-timestamp')
    #         p = Paginator(messages, 10)
    #
    #         payload = {}
    #         messages_data = None
    #         new_page_number = int(page_number)
    #         if new_page_number <= p.num_pages:
    #             new_page_number = new_page_number + 1
    #             s = LazyRoomChatMessageEncoder()
    #             payload['messages'] = s.serialize(p.page(page_number).object_list)
    #         else:
    #             payload['messages'] = 'None'
    #         payload['new_page_number'] = new_page_number
    #         return payload
    #     except Exception as e:
    #         print(e)
    #         return None

    async def chat_message(self, event):
        # send the actual message
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })


# class LazyRoomChatMessageEncoder(Serializer):
#     def get_dump_object(self, obj):
#         dump_object = {}
#         dump_object.update({'message_id': str(obj.id)})
#         dump_object.update({'user_id': str(obj.user.id)})
#         dump_object.update({'user': str(obj.user.username)})
#         dump_object.update({'message': str(obj.content)})
#         dump_object.update({'profile_image': str(obj.user.profile_image.url)})
#         dump_object.update({'timestamp': str(timezone.now())})
#         return dump_object
