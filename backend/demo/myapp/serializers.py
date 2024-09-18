from rest_framework import serializers

from .models import *


class SolarEnergyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarEnergyData
        fields = '__all__'
