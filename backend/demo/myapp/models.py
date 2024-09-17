from django.db import models

class TodoItem (models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

# Create your models here.
class SolarEnergyData(models.Model):
    #id for indexing
    timestamp = models.DateTimeField()  
    kwh=models.FloatField()
