from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import random
from .models import Post, Record, Car

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        carID = str(random.randint(10000,99999))
        self.username = carID
        async_to_sync(self.channel_layer.group_add)(
            self.username,
            self.channel_name
        )
        print(self.username)
        car = Car.objects.create(carID=self.username,carType='car', duration = 0) #,serveTime=request.POST.get('serveTime'),lastMantainTime=request.POST.get('lastMantainTime'))
        car.save()
        self.accept()
        self.send(text_data=f"[Welcome {self.username}!]")

    def disconnect(self, msg):
        async_to_sync(self.channel_layer.group_discard)(
            self.username,
            self.channel_name
        )
        print('DISCONNECT', msg)
        pass
    
    
    # receive sdp from car
    def receive(self, *, text_data):
        text_data_json = json.loads(text_data)
        car_sdp = text_data_json['message']
        target_car = Car.objects.filter(carID=self.username)
        target_car.update(sdp = car_sdp)
        
    # send sdp to car
    def chat_message(self, event):
        self.send(text_data=event["message"])
        
        
        
        
        # async_to_sync(self.channel_layer.group_send)(
        #     self.username,{
        #         "type" : "chat.message",
        #         "message" : message
        #     }
        # )
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
