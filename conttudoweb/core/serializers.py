from rest_framework import serializers

from . import models


class FederativeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FederativeUnit
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.People
        fields = '__all__'
