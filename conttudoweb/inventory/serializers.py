from rest_framework import serializers

from . import models


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnitOfMeasure
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    category__description = serializers.CharField(source='category.description', read_only=True)

    class Meta:
        model = models.Subcategory
        fields = '__all__'


class ProductSizeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.ProductSize
        exclude = ('product_size_register',)
        # fields = '__all__'


class ProductSizeRegisterSerializer(serializers.ModelSerializer):
    productsize_set = ProductSizeSerializer(many=True)

    class Meta:
        model = models.ProductSizeRegister
        fields = '__all__'

    def create(self, validated_data):
        productsize_set = validated_data.pop('productsize_set')
        product_size_register = models.ProductSizeRegister.objects.create(**validated_data)
        for productsize in productsize_set:
            models.ProductSize.objects.create(product_size_register=product_size_register, **productsize)
        return product_size_register

    # TODO: Melhorar este código!
    def update(self, instance, validated_data):
        product_size_data = validated_data.pop('productsize_set')

        for k, v in validated_data.items():
            setattr(instance, k, v)

        product_size_ids = [item.get('id') for item in product_size_data]
        for product_size in instance.productsize_set.all():
            if product_size.id not in product_size_ids:
                product_size.delete()

        product_size_list = []
        for product_size in product_size_data:
            try:
                _id = product_size.pop('id', 0)
                product_size_instance = models.ProductSize.objects.get(id=_id,
                                                                       product_size_register=instance)
                for k, v in product_size.items():
                    setattr(product_size_instance, k, v)
                product_size_instance.save()
            except models.ProductSize.DoesNotExist:
                product_size_instance = models.ProductSize.objects.create(**product_size,
                                                                          product_size_register=instance)
            product_size_list.append(product_size_instance)
        instance.productsize_set.set(product_size_list, clear=True)

        instance.save()
        return instance
