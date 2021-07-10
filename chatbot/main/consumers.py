import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .views import getjoke_response, save_counts
from . import models

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def save_calls_count(self, message):
        """
        saves calls count to each jokes available
        """
        response_model, _ = models.ResponseCount.objects.get_or_create(
            source = models.ResponseCount.ws,
            username = self.scope['user'].username
        )
        save_counts(response_model, message)
        response_model.save()

    async def connect(self):
        self.room_name = 'common-room'
        self.room_group_name = 'chat_%s' % self.room_name
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
    
    async def send_joke(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'joke',
                'message': message
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # Send message to room group
        if(text_data_json['type'] == 'joke'):
            # when user clicks a button
            message = text_data_json.get('data', 'none')
            await self.save_calls_count(message)
            await self.send_joke(message)
        elif(text_data_json['type'] == 'send'):
            # when user types in input box
            await self.save_calls_count(text_data_json['text']) # save count if it is a joke
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_msg',
                    'data': text_data_json['text']
                }
            )
            await self.send_joke(text_data_json['text'])

    # Receive message from room group
    async def user_msg(self, event):
        message = event['data']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'data': {
                'type': 'user_msg',
                'source':  'CANDIDATE',
                'text': message,
            }
        }))
    
    async def joke(self, event):
        respond_message = getjoke_response({'text': event['message']})
        await self.send(
            text_data = json.dumps({
                'data': {
                    'type': 'joke_replay',
                    'text': respond_message,
                    'source': 'BOT'
                }
            })
        )
    
    async def start(self, event):
        message = 'you have connected'
        await self.send(
            text_data = json.dumps({
                'type': 'start',
                'data': message
            })
        )