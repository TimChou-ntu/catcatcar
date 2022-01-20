from django.db import models
from django.db.models import Model 
from django.utils import timezone
from django.contrib.auth.models import User
import threading

# Create your models here.

# class MyModel(metaclass=Model):
#     _counter = 0
#     _counter_lock = threading.Lock()

#     @classmethod
#     def increment_counter(cls):
#         with cls._counter_lock:
#             cls._counter += 1

#     def some_action(self):
#         # core code 
#         self.increment_counter()

class Post(Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


### User data
class Record(Model):
    uID = models.CharField(max_length=20)
    carID = models.CharField(max_length=20)
    startTime = models.DateTimeField()
    duration = models.DurationField()

    def __str__(self):
        return f"user: {self.uID}\ncarID: {self.carID}\nstartTime: {self.startTime}\nduration: {self.duration}"

class Car(Model):
    carID = models.CharField(max_length=20)
    carType = models.CharField(max_length=20)
    carIP = models.CharField(max_length=100, default="")
    sdp = models.CharField(max_length=2048, default="")
    duration = models.IntegerField(default=0)
    hash = models.CharField(max_length=2048, default="")
    CAR_STATUS = (
        ('m', 'mantainance'),
        ('o', 'occupied'),
        ('a', 'available'),
        ('r', 'reserved')
    )
    status = models.CharField(
        max_length=1,
        choices=CAR_STATUS,
        blank=True,
        default='a',
        help_text='Car availability',
    )
    def __str__(self):
        return f"car: {self.carID} Type: {self.carType} status: {self.status}, duration: {self.duration}"