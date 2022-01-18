from django.shortcuts import render
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from queue import Queue

from .models import Post, Record, Car
from .serializers import CarSerializer
# Create your views here.
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
        car_list = Car.objects.all()
        for car in car_list:
            print("carID: ",car.carID)
            print("carType: ",car.carType)
            print("remainTime: ",car.remainTime)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            car_list[0].carID,
            {
                "type": "chat.message",
                'message' : "tim"
            }
        )
        print('send')
        return Response(data={ 'echo': '周子庭好帥' }, status=200)
        


### Render

class ClientView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)


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
                    return Response(data = "post api only accept argument with key carID or duration", status=400)
            
            target_car = Car.objects.filter(carID=carID)    #should only have one item
            if len(target_car) != 1:
                return Response(data = "this id has no car or multiple car", status=400)
            else:    
                target_car.update(duration = duration)
                return Response(data=target_car[0].sdp, status=200)
        else:
            return Response(data = "get api only accept argument two", status=400)

            
    def delete(self, request):
        car_list = Car.objects.all()
        # print(len(request.data))
        if len(request.data) == 0:
            print(car_list)
            for car in car_list:
                car.delete()
        else:
            for id in request.data:
                print(id)
                # print(request.data[key])
                Car.objects.filter(carID=id).delete()    


        return Response(data={ 'echo': 0 }, status=200)

        

class CarView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self,request):
        carID = 0
        client_sdp = 0
        
        if len(request.data) != 2:
            print(len(request.data))
            print(request.data)
            return Response(data = "this api only accept two argument", status=400)
        
        elif ('sdp' in request.data) & ('carID' in request.data):
            carID = request.data['carID']
            client_sdp = request.data['sdp']
            target_car = Car.objects.filter(carID=carID)
            if len(target_car) == 1:            
                print(carID)
                print(client_sdp)
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    carID,
                    {
                        "type": "chat.message",
                        'message' : client_sdp
                    }
                )
                print('send')
                return Response(data={'echo':'success'}, status=200)

            else:
                return Response(data = "this id has no car or multiple car", status=400)
                
        else:
            return Response(data = "argument key must be carID & sdp", status=400)
        
        
        
