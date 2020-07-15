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
