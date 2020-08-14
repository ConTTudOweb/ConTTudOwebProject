from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from . import models


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnitOfMeasure
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    str = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = models.Category
        fields = ('id', 'code', 'description', 'parent', 'str')


class SubcategorySerializer(serializers.ModelSerializer):
    category__description = serializers.CharField(source='category.description', read_only=True)
    str = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = models.Subcategory
        fields = '__all__'


class ProductSizeSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.ProductSize
        exclude = ('product_size_register',)


class ProductSizeRegisterSerializer(WritableNestedModelSerializer):
    productsize_set = ProductSizeSerializer(many=True)

    class Meta:
        model = models.ProductSizeRegister
        fields = '__all__'

    # def create(self, validated_data):
    #     productsize_set = validated_data.pop('productsize_set')
    #     product_size_register = models.ProductSizeRegister.objects.create(**validated_data)
    #     for productsize in productsize_set:
    #         models.ProductSize.objects.create(product_size_register=product_size_register, **productsize)
    #     return product_size_register
    #
    # # TODO: Melhorar este código!
    # def update(self, instance, validated_data):
    #     product_size_data = validated_data.pop('productsize_set')
    #     print(product_size_data)
    #
    #     for k, v in validated_data.items():
    #         setattr(instance, k, v)
    #
    #     product_size_ids = [item.get('id') for item in product_size_data]
    #     for product_size in instance.productsize_set.all():
    #         if product_size.id not in product_size_ids:
    #             product_size.delete()
    #
    #     product_size_list = []
    #     for product_size in product_size_data:
    #         try:
    #             _id = product_size.pop('id', 0)
    #             product_size_instance = models.ProductSize.objects.get(id=_id,
    #                                                                    product_size_register=instance)
    #             for k, v in product_size.items():
    #                 setattr(product_size_instance, k, v)
    #             product_size_instance.save()
    #         except models.ProductSize.DoesNotExist:
    #             product_size_instance = models.ProductSize.objects.create(**product_size,
    #                                                                       product_size_register=instance)
    #         product_size_list.append(product_size_instance)
    #     instance.productsize_set.set(product_size_list, clear=True)
    #
    #     instance.save()
    #     return instance


class PackagingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PackagingType
        fields = '__all__'


class ProductBySupplierSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    supplier__str = serializers.CharField(source='supplier', read_only=True)

    class Meta:
        model = models.ProductBySupplier
        exclude = ('product',)


class PackagingSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    packaging_type__str = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = models.Packaging
        exclude = ('product',)


class ProductSerializer(WritableNestedModelSerializer):
    category__str = serializers.CharField(source='category', read_only=True)
    unit_of_measure__str = serializers.CharField(source='unit_of_measure', read_only=True)
    product_size_register__str = serializers.CharField(source='product_size_register', read_only=True)
    cost_price_of_last_purchase = serializers.ReadOnlyField()

    productbysupplier_set = ProductBySupplierSerializer(many=True)
    packaging_set = PackagingSerializer(many=True)

    class Meta:
        model = models.Product
        fields = '__all__'

    # def create(self, validated_data):
    #     productbysupplier_set = validated_data.pop('productbysupplier_set')
    #     packaging_set = validated_data.pop('packaging_set')
    #
    #     product = models.Product.objects.create(**validated_data)
    #
    #     for productbysupplier in productbysupplier_set:
    #         models.ProductBySupplier.objects.create(product=product, **productbysupplier)
    #     for packaging in packaging_set:
    #         models.Packaging.objects.create(product=product, **packaging)
    #
    #     return product
    #
    # # TODO: Melhorar este código!
    # def update(self, instance, validated_data):
    #     product_by_supplier_data = validated_data.pop('productbysupplier_set')
    #     packaging_data = validated_data.pop('packaging_set')
    #
    #     for k, v in validated_data.items():
    #         setattr(instance, k, v)
    #
    #     product_by_supplier_ids = [item.get('id') for item in product_by_supplier_data]
    #     for product_by_supplier in instance.productbysupplier_set.all():
    #         if product_by_supplier.id not in product_by_supplier_ids:
    #             product_by_supplier.delete()
    #
    #     product_by_supplier_list = []
    #     for product_by_supplier in product_by_supplier_data:
    #         try:
    #             _id = product_by_supplier.pop('id', 0)
    #             product_by_supplier_instance = models.ProductBySupplier.objects.get(id=_id, product=instance)
    #             for k, v in product_by_supplier.items():
    #                 setattr(product_by_supplier_instance, k, v)
    #             product_by_supplier_instance.save()
    #         except models.ProductBySupplier.DoesNotExist:
    #             product_by_supplier_instance = models.ProductBySupplier.objects.create(**product_by_supplier,
    #                                                                                    product=instance)
    #         product_by_supplier_list.append(product_by_supplier_instance)
    #     instance.productbysupplier_set.set(product_by_supplier_list, clear=True)
    #
    #     packaging_ids = [item.get('id') for item in packaging_data]
    #     for packaging in instance.packaging_set.all():
    #         if packaging.id not in packaging_ids:
    #             packaging.delete()
    #
    #     packaging_list = []
    #     for packaging in packaging_data:
    #         try:
    #             _id = packaging.pop('id', 0)
    #             packaging_instance = models.Packaging.objects.get(id=_id, product=instance)
    #             for k, v in packaging.items():
    #                 setattr(packaging_instance, k, v)
    #             packaging_instance.save()
    #         except models.Packaging.DoesNotExist:
    #             packaging_instance = models.Packaging.objects.create(**packaging, product=instance)
    #         packaging_list.append(packaging_instance)
    #     instance.packaging_set.set(packaging_list, clear=True)
    #
    #     instance.save()
    #     return instance
