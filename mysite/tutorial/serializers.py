from dataclasses import field
from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    carID = serializers.CharField(max_length=20)
    carType = serializers.CharField(max_length=20)
    status = serializers.CharField(max_length=1)
    
    class Meta:
        model = Car
        fields = ['carID', 'carType', 'status','duration']
        
class TokenReturnSerializer(serializers.ModelSerializer):
    carID = serializers.CharField(max_length=20)
    carIP = serializers.CharField(max_length=100)
    sdp = serializers.CharField(max_length=2048)
    
    class Meta:
        model = Car
        fields = ["carID", "carIP", "sdp"]
