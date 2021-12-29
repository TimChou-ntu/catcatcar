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