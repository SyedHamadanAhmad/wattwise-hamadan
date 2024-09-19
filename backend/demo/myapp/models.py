from django.db import models


class SolarEnergyData(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    kwh = models.FloatField()
