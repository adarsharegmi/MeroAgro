import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'chat_%s' % self.room_name

        print("print connected")
        # once it is connected lets send the messages from database

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("the text data is",text_data)
        text_data_json = json.loads(text_data)

        message = text_data_json['message']

        # save the message into the database
        @sync_to_async
        def save_message(self):
            user,created = User.objects.get_or_create(id=self.user_id)
            room,created = Room.objects.get_or_create(room_name=self.room_name)
            room.user.add(user)
            # ru = RoomUser.objects.get_or_create(user=user,room=room)
            return Message(messageText=message,messageDate=datetime.datetime.now(),user_room=room,user=user).save()

        await save_message(self)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user':self.user_id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user':user
        }))