from django.shortcuts import render
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


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
        print(Post.objects.all().empty())
        
        post1 = Post(title='12',content='23')
        post1.save()
        
        return Response(data={ 'echo': '周子庭好帥' }, status=200)
        
        return Response(data={ 'echo': 'queue' }, status=200)


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
        for car in car_list:
            print("carID: ",car.carID)
            print("carType: ",car.carType)
            print("status: ",car.status)
            # car.delete()
            
       
        return Response(data=serializer.data, status=200)
    
    def post(self, request):
        for key, value in request.POST.items():
            print('Key: %s' % (key) ) 
            # print(f'Key: {key}') in Python >= 3.7
            print('Value %s' % (value) )
            # print(f'Value: {value}') in Python >= 3.7
        # if not Car.objects.all():
        print(request.POST.get('carID'))
        print(request.POST.get('carType'))
        # print(request.POST.get('serveTime'))
        # print(request.POST.get('lastMantainTime'))
        car = Car.objects.create(carID=request.POST.get('carID'),carType=request.POST.get('carType'),remainTime=request.POST.get('remainTime')) #,serveTime=request.POST.get('serveTime'),lastMantainTime=request.POST.get('lastMantainTime'))
        car.save()
        return Response(data={ 'echo': '好帥' }, status=200)
        

class CarView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self,request):
        print(request.POST.get('carID'))
        mycars = Car.objects.filter(carID=request.POST.get('carID'))            
        for mycar in mycars:
            remainTime = request.POST.get('remainTime')
            status = request.POST.get('status')
            mycar.remainTime = remainTime
            mycar.status = status
            mycar.save()
        return Response(data = {'echo':'car updated'},status=200)
        return Response(data={ 'echo': 'you so fucking sad'}) 