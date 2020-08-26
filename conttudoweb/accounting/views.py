from . import models
from . import serializers
from ..core.views import CustomModelViewSet


class AccountPayableViewSet(CustomModelViewSet):
    """
    ** Contas a Pagar **
    """
    serializer_class = serializers.AccountPayableSerializer
    queryset = models.AccountPayable.objects.all().order_by('due_date')
    search_fields = ['document', 'description', 'category__description', 'observation', 'person__name',
                     'classification_center__description']


class CategoryViewSet(CustomModelViewSet):
    """
    ** Categoria de Contas **
    """
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    search_fields = ['description']


class BankViewSet(CustomModelViewSet):
    """
    ** Banco **
    """
    serializer_class = serializers.BankSerializer
    queryset = models.Bank.objects.all()
    search_fields = ['code', 'description']


class DepositAccountViewSet(CustomModelViewSet):
    """
    ** Conta Financeira **
    """
    serializer_class = serializers.DepositAccountSerializer
    queryset = models.DepositAccount.objects.all()
    search_fields = ['bank__code', 'bank__description', 'agency_number', 'account_number', 'name']


class ClassificationCenterViewSet(CustomModelViewSet):
    """
    ** Centros de Custo/Despesa **
    """
    serializer_class = serializers.ClassificationCenterSerializer
    queryset = models.ClassificationCenter.objects.all()
    search_fields = ['name']
    filterset_fields = ['cost_center', 'revenue_center']
