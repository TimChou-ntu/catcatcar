from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import random
from .models import Post, Record, Car
import codecs
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        carID = str(random.randint(10000,99999))
        self.username = carID
        async_to_sync(self.channel_layer.group_add)(
            self.username,
            self.channel_name
        )
        print(self.username)
        car = Car.objects.create(carID=self.username,carType='car', carIP = "192.168.137.58", duration = 0) #,serveTime=request.POST.get('serveTime'),lastMantainTime=request.POST.get('lastMantainTime'))
        car.save()
        self.accept()
        # self.send(text_data=f"[Welcome {self.username}!]")

    def disconnect(self, msg):
        async_to_sync(self.channel_layer.group_discard)(
            self.username,
            self.channel_name
        )
        target_car = Car.objects.filter(carID=self.username)
        target_car.update(status='m')
        print('DISCONNECT', msg)
        pass
    
    
    # receive sdp from car
    def receive(self, *, text_data):
        # text_data_json = json.loads(text_data)
        print(text_data)
        # print(text_data)
        # print(text_data_json)
        # car_sdp = text_data_json
        # print(type(car_sdp))
        # car_sdp = car_sdp.replace("\\\\","\\")
        # print(car_sdp['sdp'])
        target_car = Car.objects.filter(carID=self.username)
        # target_car.update(sdp = codecs.decode(text_data, 'unicode_escape'))
        # target_car.update(sdp = codecs.decode(text_data, 'unicode_escape'))
        # data = json.loads(text_data)
        # timeout = data['timeout']
        # print(timeout)
        # sdp_data = json.dumps({
        #     'sdp': data['sdp'],
        #     'type' : data['type']
        # })
        # target_car.update(sdp = sdp_data)
        message = json.loads(text_data)
        # data = {"sdp": str(message['sdp']), "type": message['type']}        
        if 'timeout' in message:
            if message['timeout'] == True:
                print("receive timeout")
                target_car.update(status='a')
                target_car.update(hash='')
        target_car.update(sdp = message['sdp'])
        
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
