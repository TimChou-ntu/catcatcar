import re
from django.shortcuts import render
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from queue import Queue
import codecs
import time
import threading
import json
import hashlib
from aiortc import RTCSessionDescription
from .models import Post, Record, Car
from .serializers import CarSerializer, TokenReturnSerializer
# Create your views here.
TOKEN_VALID_TIME = 30000
time_list = []


def func():
    global time_list
    while True:
        time.sleep(1)
        if time_list:
            for i in time_list:
                car, t = i
                if time.time() >= t:
                    print("timeout") 
                    if car[0].status == 'r':
                        car.update(status = 'a')
                        car.update(hash = '')
                    time_list.remove(i)
    # print("hello {} timer!".format(num))
    

class EchoView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    # def post(self, request):
    #     global q 
    #     q = Queue()

    #     return Response(data={ 'echo': 'queue' }, status=200)
    def __init__(self):
        print(Post.objects.all())
        return 

       
    def get(self, request):
        global time_list
        # car_list = Car.objects.all()
        # for car in car_list:
        #     print("carID: ",car.carID)
        #     print("carType: ",car.carType)
        #     print("remainTime: ",car.remainTime)

        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     car_list[0].carID,
        #     {
        #         "type": "chat.message",
        #         'message' : "tim"
        #     }
        # )
        # timer = threading.Timer(5, func, (1,))
        # timer0 = time.time()
        # timer.start()
        # print(time.time() - timer0)
        car = Car.objects.create(carID="test",carType='car', carIP = "192.168.122.58", duration = 0, sdp = "jjj") #,serveTime=request.POST.get('serveTime'),lastMantainTime=request.POST.get('lastMantainTime'))
        car.save()

        data = json.dumps({
            "jj":"jj",
            "gg":"gg"
        })
        print('send')
        return Response(data=data, status=200)
        


### Render

class ClientView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    t = threading.Thread(target = func)
    t.start()



    def get(self, request):
        fromip = request.META.get("REMOTE_ADDR")
        print(f"receive req from {fromip}")
        car_list = Car.objects.all()
        serializer = CarSerializer(car_list, many=True)
        print(car_list)
        if len(car_list) == 0:
            print('no_car')
        else:
            for car in car_list:
                print("carID: ",car.carID)
                print("carType: ",car.carType)
                print("status: ",car.status)
                print("hash: ", car.hash)
        return Response(data=serializer.data, status=200)
    
    def post(self, request):
        carID = 0
        duration = 0
        if len(request.data) == 2:
            for key in request.data:
                print(key, request.data[key])
                if key == 'carID':
                    carID = request.data[key]
                elif key == 'duration':
                    duration = request.data[key]
                else:
                    return Response(data = {"message":"post api only accept argument with key carID or duration"}, status=400)
            
            target_car = Car.objects.filter(carID=carID)    #should only have one item
            if len(target_car) != 1:
                return Response(data = {"message":"this id has no car or multiple car"}, status=400)
            elif target_car[0].status != 'a':
                return Response(data = {"message":"this car is not available"}, status=400)
            else:    
                time_list.append((target_car, time.time() + TOKEN_VALID_TIME))

                m = hashlib.md5()
                target_car.update(duration = duration)
                print(target_car[0].sdp)
                # print({'sdp': {}, 'type': 'offer'}.format(target_car[0].sdp))
                print(type(target_car[0].sdp))
                # data = json.loads(target_car[0].sdp)
                m.update(target_car[0].sdp.encode("utf-8"))
                data = m.hexdigest()
                target_car.update(hash = data)
                target_car.update(status = 'r')
                # data = codecs.decode(target_car[0].sdp, 'unicode_escape').split("sdp\": \"")[1].split("\", \"type")[0]
                # data = target_car[0].sdp.replace("\"","")
                # d["sdp"] = data
                # d["type"] = "offer"
                # print(d)
                return Response(data=data, status=200)
        else:
            return Response(data = {"message":"get api only accept argument two"}, status=400)

            
    def delete(self, request):
        car_list = Car.objects.all()
        # print(len(request.data))
        # if len(request.data) == 0:
        if True:
            print(car_list)
            for car in car_list:
                car.delete()
        else:
            for id in request.data:
                print(id)
                # print(request.data[key])
                Car.objects.filter(carID=id).delete()    


        return Response(data={ 'echo': 0 }, status=200)

class CarDetailView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self,request, token_id):
        target_car = Car.objects.filter(hash=token_id)
        if len(target_car) == 1:
            serializer = TokenReturnSerializer(target_car, many=True)
            return Response(data=serializer.data, status=200)
        else:
            return Response(data = {"message":"this token is not valid"}, status=400)


class CarView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    # def get(self,request):
    #     if (len(request.data) == 1) & ("token" in request.data):
    #         target_car = Car.objects.filter(hash=request.data["token"])
    #         if len(target_car) == 1:
    #             serializer = TokenReturnSerializer(target_car, many=True)
    #             return Response(data=serializer.data, status=200)
    #         else:
    #             return Response(data = "this token is not valid", status=400)
    #     else:
    #         return Response(data = "car/get api only accept argument one", status=400)
    
    def post(self,request):
        carID = 0
        client_sdp = 0
        
        request_dict = json.loads(request.data)
        
        if len(request_dict) != 2:
            print(len(request_dict))
            print("here")
            print(request_dict)
            return Response(data = {"message":"this api only accept two argument"}, status=400)
        
        elif ('sdp' in request_dict) & ('carID' in request_dict):
            carID = request_dict['carID']
            # client_sdp = json.loads(request_dict['sdp'])
            client_sdp = request_dict['sdp']
            target_car = Car.objects.filter(carID=carID)
            print(carID)
            print(client_sdp)

            if len(target_car) == 1:            
                target_car.update(status='o')
                print(carID)
                print(client_sdp)
                channel_layer = get_channel_layer()
                obj = json.dumps({
                    "sdp": client_sdp,
                    "duration": target_car[0].duration
                })
                # obj = json.dumps({
                #     "sdp": client_sdp,
                #     "duration": target_car[0].duration
                # })
                print(obj)
                async_to_sync(channel_layer.group_send)(
                    carID,
                    {
                        "type": "chat.message",
                        'message' : obj
                    }
                )
                print('send')
                return Response(data={"message":'success'}, status=200)

            else:
                print(len(target_car))
                return Response(data = {"message":"this id has no car or multiple car"}, status=400)
                
        else:
            return Response(data = {"message":"argument key must be carID & sdp"}, status=400)
        
        
        
