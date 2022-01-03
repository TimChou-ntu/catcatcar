from django.contrib import admin

from .models import Car, Record
# Register your models here.

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ( 'uID', 'carID', 'startTime', 'duration')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass