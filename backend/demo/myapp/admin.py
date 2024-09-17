from django.contrib import admin

# Register your models here.
from .models import TodoItem
from .models import SolarEnergyData

admin.site.register(TodoItem)
admin.site.register(SolarEnergyData)
