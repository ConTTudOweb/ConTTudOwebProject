from rest_framework import viewsets
from django_filters import rest_framework as filters

from . import serializers
from . import models


class FederativeUnitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FederativeUnitSerializer
    queryset = models.FederativeUnit.objects.all()


class CityFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.City
        fields = ('name',)


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CitySerializer
    queryset = models.City.objects.all()
    # filterset_fields = '__all__'
    filterset_class = CityFilter


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PeopleSerializer
    queryset = models.People.objects.all()
