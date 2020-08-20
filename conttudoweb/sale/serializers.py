from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from . import models


class SaleOrderItemsSerializer(serializers.ModelSerializer):
    product__str = serializers.CharField(source='product', read_only=True)
    packaging_type = serializers.ReadOnlyField(source='packing.packaging_type.id')
    packaging__quantity = serializers.ReadOnlyField(source='packing.quantity')

    class Meta:
        model = models.SaleOrderItems
        exclude = ('sale_order',)


class SaleOrderSerializer(WritableNestedModelSerializer):
    customer__str = serializers.CharField(source='customer', read_only=True)

    saleorderitems_set = SaleOrderItemsSerializer(many=True)

    net_total = serializers.ReadOnlyField()

    class Meta:
        model = models.SaleOrder
        fields = '__all__'
