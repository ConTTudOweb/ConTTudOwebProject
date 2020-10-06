from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response

from . import models
from . import serializers
from ..core.views import CustomModelViewSet


class AccountPayableViewSet(CustomModelViewSet):
    """
    ** Contas a Pagar **
    """
    serializer_class = serializers.AccountPayableSerializer
    queryset = models.AccountPayable.objects.order_by('-id')
    search_fields = ['document', 'description', 'category__description', 'observation', 'person__name',
                     'classification_center__name']


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


class AccountsPayableByDueDateViewSet(viewsets.ViewSet):
    """
    list:\n
    Retorna uma lista de todas as contas a pagar filtradas por vencimento.\n

    params:\n
        **start_date**: Data inicial
        **end_date**: Data final
    """

    queryset = models.AccountPayable.objects.none()

    def list(self, request):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        _filter = Q()
        if start_date:
            _filter &= Q(due_date__gte=start_date)
        if end_date:
            _filter &= Q(due_date__lte=end_date)

        contas = models.AccountPayable.objects.filter(_filter).values(
            'due_date', 'description', 'amount'
        ).order_by('due_date')

        data = {
            'start_date': start_date,
            'end_date': end_date,
            'results': contas
        }

        return Response(data, status=status.HTTP_200_OK)
