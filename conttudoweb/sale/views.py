import datetime
import itertools
import operator

from rest_framework import viewsets
from rest_framework.response import Response

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


class SalesByProductViewSet(viewsets.ViewSet):
    # serializer_class = serializers.SalesByProductSerializer
    queryset = models.SaleOrder.objects.none()

    # def get_queryset(self):
    #     return SaleOrder.objects.all()

    def list(self, request):
        data = datetime.date.today()
        pedidos = models.SaleOrderItems.objects.filter(
            sale_order__date_order__lte=data
        ).values(
            'product__description', 'sale_order__date_order', 'quantity', 'packing__quantity'
        ).order_by('product__description')
        rows = itertools.groupby(pedidos, operator.itemgetter('product__description'))

        results = []
        for c_title, items in rows:
            results.append({
                'produto': c_title,
                'detalhes': list(items)
            })

        # pedidos = self.serializer_class(pedidos, many=True)

        return Response({
            # 'data_inicial': request.query_params.get('data_inicial', None),
            # 'queryset': pedidos,
            'results': results
        })
