from rest_framework import serializers

from . import models


class FederativeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FederativeUnit
        fields = '__all__'
