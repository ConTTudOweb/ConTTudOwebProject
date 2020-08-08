from . import models
from . import serializers
from ..core.views import CustomModelViewSet


class SaleOrderViewSet(CustomModelViewSet):
    """
    ** Ordem de Venda **
    """
    serializer_class = serializers.SaleOrderSerializer
    queryset = models.SaleOrder.objects.all()
    search_fields = ['code', 'description', 'ncm']
