# Consumers for Django Channels Websocket connections - Desk Reservations

import pdb
from turtle import pd
from asgiref.sync import async_to_sync
from distutils.log import debug
import json

from channels.generic.websocket import WebsocketConsumer


class DeskReservationConsumer(WebsocketConsumer):
    def connect(self):
        self.building = self.scope['url_route']['kwargs']['building']
        self.floor = self.scope['url_route']['kwargs']['floor']
        self.screen_group_name = 'screen_%s_%s' % (self.building, self.floor)

        # Join floor screen group
        async_to_sync(self.channel_layer.group_add)(
            self.screen_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave floor screen group
        async_to_sync(self.channel_layer.group_discard)(
            self.screen_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to floor screen group
        async_to_sync(self.channel_layer.group_send)(
            self.screen_group_name,
            {
                'type': 'screen_group_message',
                'message': message
            }
        )
    
    # Receive message from floor screen group
    def screen_group_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))