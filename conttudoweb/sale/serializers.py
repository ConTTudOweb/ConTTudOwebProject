from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from . import models


class SaleOrderItemsSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    product__str = serializers.CharField(source='product', read_only=True)

    class Meta:
        model = models.SaleOrderItems
        exclude = ('sale_order',)


class SaleOrderSerializer(WritableNestedModelSerializer):
    customer__str = serializers.CharField(source='customer', read_only=True)

    saleorderitems_set = SaleOrderItemsSerializer(many=True)

    class Meta:
        model = models.SaleOrder
        fields = '__all__'

    # def create(self, validated_data):
    #     saleorderitems_set = validated_data.pop('saleorderitems_set')
    #     sale_order = models.SaleOrder.objects.create(**validated_data)
    #     for saleorderitem in saleorderitems_set:
    #         models.SaleOrderItems.objects.create(sale_order=sale_order, **saleorderitem)
    #     return sale_order
    #
    # # TODO: Melhorar este código!
    # def update(self, instance, validated_data):
    #     sale_order_items_data = validated_data.pop('saleorderitems_set')
    #
    #     for k, v in validated_data.items():
    #         setattr(instance, k, v)
    #
    #     print('sale_order_items_data:')
    #     print(sale_order_items_data)
    #     print('---')
    #     sale_order_items_ids = [item.get('id') for item in sale_order_items_data]
    #     print('sale_order_items_ids:')
    #     print(sale_order_items_ids)
    #     print('---')
    #     print('instance.saleorderitems_set.all():')
    #     print(instance.saleorderitems_set.all())
    #     print('---')
    #     for sale_order_item in instance.saleorderitems_set.all():
    #         if sale_order_item.id not in sale_order_items_ids:
    #             sale_order_item.delete()
    #
    #     sale_order_items_list = []
    #     for sale_order_items in sale_order_items_data:
    #         try:
    #             _id = sale_order_items.pop('id', 0)
    #             sale_order_items_instance = models.SaleOrderItems.objects.get(id=_id, sale_order=instance)
    #             for k, v in sale_order_items.items():
    #                 setattr(sale_order_items_instance, k, v)
    #             sale_order_items_instance.save()
    #         except models.SaleOrderItems.DoesNotExist:
    #             sale_order_items_instance = models.SaleOrderItems.objects.create(**sale_order_items,
    #                                                                              sale_order=instance)
    #         sale_order_items_list.append(sale_order_items_instance)
    #     instance.saleorderitems_set.set(sale_order_items_list, clear=True)
    #
    #     instance.save()
    #     return instance
