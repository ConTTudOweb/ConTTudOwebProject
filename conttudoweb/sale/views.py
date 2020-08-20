import datetime
import itertools
import operator

from django.db.models import Window, Sum, F
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
    search_fields = ['customer__name', 'id']


class SalesByProductViewSet(viewsets.ViewSet):
    # serializer_class = serializers.SalesByProductSerializer
    queryset = models.SaleOrder.objects.none()

    # def get_queryset(self):
    #     return SaleOrder.objects.all()

    def list(self, request):
        data = datetime.date.today()
        # pedidos = models.SaleOrderItems.objects.filter(
        #     sale_order__date_order__lte=data
        # ).values(
        #     'product__description', 'sale_order__date_order', 'quantity', 'packing__quantity'
        # ).order_by('product__description')
        pedidos = models.SaleOrderItems.objects.filter(
            sale_order__date_order__lte=data
        ).annotate(
            quantity__sum=Window(
                expression=Sum('quantity'),
                partition_by=[F('product__description')],
                order_by=F('product__description').asc()
            ),
            net_total__sum=Window(
                expression=Sum('net_total'),
                partition_by=[F('product__description')],
                order_by=F('product__description').asc()
            ),
        ).values(
            'product__description', 'quantity__sum', 'net_total__sum', 'sale_order__date_order', 'quantity',
            'net_total', 'packing__quantity'
        ).order_by('product__description')
        # rows = itertools.groupby(pedidos, operator.itemgetter('product__description'))
        rows = itertools.groupby(pedidos, operator.itemgetter('product__description', 'quantity__sum', 'net_total__sum'))

        results = []
        for c_title, items in rows:
            results.append({
                'product__description': c_title[0],
                'quantity__sum': c_title[1],
                'net_total__sum': c_title[2],
                'details': list(items)
            })


        #######################

        # itens = models.SaleOrderItems.objects.filter(
        #     sale_order__date_order__lte=data
        # ).values(
        #     'product__description', 'sale_order__date_order', 'quantity', 'packing__quantity'
        # ).order_by('product__description', 'sale_order__date_order')
        #
        # results = []
        # _produto = None
        # for item in itens:
        #     if _produto != item.get('product__description'):
        #         _produto = item.get('product__description')
        #         results.append({
        #             'produto': _produto
        #         })


        return Response({
            # 'data_inicial': request.query_params.get('data_inicial', None),
            # 'queryset': pedidos,
            'results': results
        })
