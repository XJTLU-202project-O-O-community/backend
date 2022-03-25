# chat/consumers.py
import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import MessageList, MessageModel


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_name = "{}".format(user_id)

        # Join room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        '''
            text_data: {
                            user_id: 1,
                            recipient_id: 2,
                            message: "hello"
                        }
        '''
        text_data_json = json.loads(text_data)
        print(text_data_json)
        user_id = text_data_json['user_id']
        recipient_id = text_data_json['recipient_id']
        message = text_data_json['message'].strip()

        msg = await self.saveMsg(user_id=user_id, recipient_id=recipient_id, message=message)

        notification = {
            'user_id': msg.room.user_id,
            'recipient_id': msg.room.recipient_id,
            "id": msg.id,
            "message": msg.message,
            "createdAt": msg.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
        }

        # Send message to room group
        await self.channel_layer.group_send(
            "{}".format(msg.room.user_id),
            {
                'type': 'chat_message',
                'message': notification
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print(event, 888888)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def saveMsg(self, user_id=None, recipient_id=None, message=None):
        room = MessageList.objects.get_or_create(user_id=user_id, recipient_id=recipient_id)[0]
        msg = MessageModel.objects.create(room=room, message=message)
        msg.save()
        return msg
