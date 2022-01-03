from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    carID = serializers.CharField(max_length=20)
    carType = serializers.CharField(max_length=20)
    status = serializers.CharField(max_length=1)
    
    class Meta:
        model = Car
        fields = ['carID', 'carType', 'status']