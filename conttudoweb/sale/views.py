import datetime
import itertools
import operator

from django.db.models import Window, Sum, F, Q
from rest_framework import viewsets, status
from rest_framework.response import Response

from . import models
from . import serializers
from ..core.views import CustomModelViewSet


class SaleOrderViewSet(CustomModelViewSet):
    """
    ** Ordem de Venda **
    """
    serializer_class = serializers.SaleOrderSerializer
    queryset = models.SaleOrder.objects.order_by('-id')
    search_fields = ['customer__name', 'id']


class SalesByProductViewSet(viewsets.ViewSet):
    """
    list:\n
    Retorna uma lista de todas as vendas agrupadas por produto.\n

    params:\n
        **start_date_order**: Data inicial
        **end_date_order**: Data final
    """

    queryset = models.SaleOrder.objects.none()

    def list(self, request):
        start_date_order = request.query_params.get('start_date_order', None)
        end_date_order = request.query_params.get('end_date_order', None)
        _filter = Q()
        if start_date_order:
            _filter &= Q(sale_order__date_order__gte=start_date_order)
        if end_date_order:
            _filter &= Q(sale_order__date_order__lte=end_date_order)

        pedidos = models.SaleOrderItems.objects.filter(_filter).annotate(
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
        ).order_by('product__description', 'sale_order__date_order')
        rows = itertools.groupby(
            pedidos, operator.itemgetter('product__description', 'quantity__sum', 'net_total__sum')
        )

        results = []
        for c_title, items in rows:
            results.append({
                'product__description': c_title[0],
                'quantity__sum': c_title[1],
                'net_total__sum': c_title[2],
                'details': list(items)
            })

        data = {
            'start_date_order': start_date_order,
            'end_date_order': end_date_order,
            'results': results
        }

        return Response(data, status=status.HTTP_200_OK)
