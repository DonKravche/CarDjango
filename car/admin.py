from django.contrib import admin
from . models import Manufacturer, Model, CarGeneration, Car


# Register your models here.

admin.site.register(Manufacturer)
admin.site.register(Model)
admin.site.register(CarGeneration)
admin.site.register(Car)