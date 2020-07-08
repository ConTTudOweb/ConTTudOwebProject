from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from . import models
from . import serializers


class CustomModelViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)


class FederativeUnitViewSet(CustomModelViewSet):
    """
    ** Unidades Federativas **
    """
    serializer_class = serializers.FederativeUnitSerializer
    queryset = models.FederativeUnit.objects.all()
    search_fields = ['initials', 'name']


# class CityFilter(filters.FilterSet):
#     name = filters.CharFilter(lookup_expr='icontains')
#
#     class Meta:
#         model = models.City
#         fields = ('name',)


class CityViewSet(CustomModelViewSet):
    """
    ** Cidades **
    """
    serializer_class = serializers.CitySerializer
    queryset = models.City.objects.all()
    # filterset_class = CityFilter
    search_fields = ['name', 'uf__initials']


class PeopleViewSet(CustomModelViewSet):
    """
    ** Pessoas (Clientes e Fornecedores) **
    """
    serializer_class = serializers.PeopleSerializer
    queryset = models.People.objects.all()
    search_fields = ['name']
