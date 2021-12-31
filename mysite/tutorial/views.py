from django.shortcuts import render
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


from queue import Queue

from .models import Post

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

class CarView(APIView):
    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request):
        return Response(data={ 'echo': '周子庭好帥' }, status=200)
