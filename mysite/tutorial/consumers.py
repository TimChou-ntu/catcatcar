from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.username = self.scope["user"]
        self.accept()
        self.send(text_data="[Welcome %s!]" % self.username)

    def disconnect(self, msg):
        pass

    def receive(self, *, text_data):
        text_data_json = json.loads(text_data)
        message = 'fuck' + text_data_json['message']
        self.send(text_data=json.dumps({
            'message': message
        }))