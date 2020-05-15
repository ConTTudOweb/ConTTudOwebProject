from rest_framework import serializers

from . import models


class FederativeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FederativeUnit
        fields = '__all__'


class FederativeUnitField(serializers.RelatedField):
    def to_representation(self, value):
        return str(value)


class CitySerializer(serializers.ModelSerializer):
    uf__initials = serializers.CharField(source='uf.initials', read_only=True)

    class Meta:
        model = models.City
        fields = '__all__'


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.People
        fields = '__all__'
