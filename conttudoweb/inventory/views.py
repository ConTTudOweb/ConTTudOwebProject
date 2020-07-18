from . import models
from . import serializers
from ..core.views import CustomModelViewSet


class UnitOfMeasureViewSet(CustomModelViewSet):
    """
    ** Unidades de Medida **
    """
    serializer_class = serializers.UnitOfMeasureSerializer
    queryset = models.UnitOfMeasure.objects.all()
    search_fields = ['initials', 'description']


class CategoryViewSet(CustomModelViewSet):
    """
    ** Categoria de Produtos **
    """
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    search_fields = ['code', 'description']


class SubcategoryViewSet(CustomModelViewSet):
    """
    ** Subcategoria de Produtos **
    """
    serializer_class = serializers.SubcategorySerializer
    queryset = models.Subcategory.objects.all()
    search_fields = ['code', 'description', 'category__description']


class ProductSizeRegisterSerializerViewSet(CustomModelViewSet):
    """
    ** Grade de Produtos **
    """
    serializer_class = serializers.ProductSizeRegisterSerializer
    queryset = models.ProductSizeRegister.objects.all()
    search_fields = ['description', ]
