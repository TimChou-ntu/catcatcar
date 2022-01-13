from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import random

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.username = self.scope["user"]
        # print(self.username)
        random.randint(10000,99999)
        self.username = str(random.randint(10000,99999))
        self.user_group_name = self.username+'_sharif'
        async_to_sync(self.channel_layer.group_add)(
            self.user_group_name,
            self.channel_name
        )
        print(self.user_group_name)
        self.accept()
        self.send(text_data=f"[Welcome {self.user_group_name}!]")

    def disconnect(self, msg):
        async_to_sync(self.channel_layer.group_discard)(
            self.user_group_name,
            self.channel_name
        )
        print('DISCONNECT', msg)
        pass

    def receive(self, *, text_data):
        text_data_json = json.loads(text_data)
        message = 'fuck' + text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.user_group_name,{
                "type" : "chat.message",
                "message" : message
            }
        )
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
    def chat_message(self, event):
        self.send(text_data=event["message"])