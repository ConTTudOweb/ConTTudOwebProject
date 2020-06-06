from django_filters import rest_framework as filters
from rest_framework import viewsets

from . import models
from . import serializers
from .utils import federative_unit_verbose_name


class FederativeUnitViewSet(viewsets.ModelViewSet):
    """
    ** Unidades Federativas **
    """
    serializer_class = serializers.FederativeUnitSerializer
    queryset = models.FederativeUnit.objects.all()


class CityFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.City
        fields = ('name',)


class CityViewSet(viewsets.ModelViewSet):
    """
    ** Cidades **
    """
    serializer_class = serializers.CitySerializer
    queryset = models.City.objects.all()
    filterset_class = CityFilter


class PeopleViewSet(viewsets.ModelViewSet):
    """
    ** Pessoas (Clientes e Fornecedores) **
    """
    serializer_class = serializers.PeopleSerializer
    queryset = models.People.objects.all()
