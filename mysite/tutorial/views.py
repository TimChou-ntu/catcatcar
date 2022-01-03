from django.shortcuts import render
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


from queue import Queue

from .models import Post, Record,Car

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
    permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.AllowAny,)

    

    def get(self, request):
        print(request.user)
        return Response(data={ 'echo': '周子庭好帥' }, status=200)
class CarView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self,request):
        print(request.POST.get('carID'))
        mycars = Car.objects.filter(carID=request.POST.get('carID'))
        # if not mycars:
            
        for mycar in mycars:
            remainTime = request.POST.get('remainTime')
            status = request.POST.get('status')
            mycar.remainTime = remainTime
            mycar.status = status
            mycar.save()
            return Response(data = {'echo':'car updated'},status=200)
        return Response(data={ 'echo': 'you so fucking sad'}) 