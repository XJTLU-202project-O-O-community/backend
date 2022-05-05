# chat/consumers.py
import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import MessageList, MessageModel


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.target_user_id = None
        self.room_name = None

    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_name = "{}".format(user_id)
        print("【CONNECT】---", self.room_name)
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
        print("【RECEIVE MESSAGE】", text_data_json)
        user_id = text_data_json['user_id']
        recipient_id = text_data_json['recipient_id']

        message = text_data_json['message'].strip()
        has_read = False

        msg = await self.saveMsg(user_id=user_id, recipient_id=recipient_id, message=message, has_read=has_read)

        notification = {
            'user_id': msg.room.user_id,
            'recipient_id': msg.room.recipient_id,
            "id": msg.id,
            "message": msg.message,
            "createdAt": msg.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
        }
        # Send message to room group
        await self.channel_layer.group_send(
            "{}".format(msg.room.recipient_id),
            {
                'type': 'chat_message',
                'id': msg,
                'message': notification
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        msg = await self.updateMsg(id=event['id'])
        print("【UPDATE MESSAGE】", msg)

        # Send message to WebSocket
        print("【SEND MESSAGE】", event['message'])
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def saveMsg(self, user_id=None, recipient_id=None, message=None, has_read=None):
        room = MessageList.objects.get_or_create(user_id=user_id, recipient_id=recipient_id)[0]
        msg = MessageModel.objects.create(room=room, message=message, hasRead=has_read)
        msg.save()
        print("【SAVE MESSAGE】", msg)
        return msg

    @database_sync_to_async
    def updateMsg(self, id=None):
        try:
            message_model = MessageModel.objects.get(id=id)
            if message_model.room__user_id == self.target_user_id:
                message_model.hasRead = True
                message_model.save()
            return message_model
        except MessageModel.DoesNotExist as e:
            print(e)
        except MessageModel.MultipleObjectsReturned as e:
            print(e)
        except Exception as e:
            print(e)
        return None

    async def change_target(self, event):
        print("【CHANGE TARGET】", event)
        self.target_user_id = event['target_user_id']
