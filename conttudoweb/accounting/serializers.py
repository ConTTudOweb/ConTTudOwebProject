from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from . import models


class AccountPayableSerializer(serializers.ModelSerializer):
    category__str = serializers.CharField(source='category', read_only=True)
    person__str = serializers.CharField(source='person', read_only=True)
    expected_deposit_account__str = serializers.CharField(source='expected_deposit_account', read_only=True)

    class Meta:
        model = models.AccountPayable
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    str = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = models.Category
        fields = ('id', 'str', 'description', 'parent')


class BankSerializer(serializers.ModelSerializer):
    str = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = models.Bank
        fields = '__all__'


class DepositAccountSerializer(WritableNestedModelSerializer):
    type_display = serializers.ReadOnlyField(source='get_type_display')
    agency_display = serializers.ReadOnlyField()
    account_display = serializers.ReadOnlyField()
    bank__str = serializers.CharField(source='bank', read_only=True)

    def validate(self, data):
        """
        Quanto o tipo for "Conta corrente" deve obrigar a preencher o banco.
        Quando o tipo não é "Conta corrente" o banco não deve estar preenchido.
        """
        # Quanto o tipo for "Conta corrente" deve obrigar a preencher o banco.
        if data['type'] == models.DepositAccount.DepositAccountTypes.current_account.value and data['bank'] is None:
            raise serializers.ValidationError(
                'O "' + models.DepositAccount._meta.get_field('bank').verbose_name +
                '" deve ser preenchido quando o "Tipo" for "Conta corrente"!'
            )
        # Quando o tipo não é "Conta corrente" o banco não deve estar preenchido.
        if data['type'] != models.DepositAccount.DepositAccountTypes.current_account.value:
            data['bank'] = None
            data['agency_number'] = None
            data['agency_digit'] = None
            data['account_number'] = None
            data['account_digit'] = None

        return data

    class Meta:
        model = models.DepositAccount
        fields = '__all__'


class ClassificationCenterSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Ao menos uma das opções deve ser escolhida! "centro de custo" ou "centro de receita".
        """
        # Ao menos uma das opções deve ser escolhida! "centro de custo" ou "centro de receita"
        if data.get('cost_center', False) is False and data.get('revenue_center', False) is False:
            raise serializers.ValidationError(
                'Ao menos uma das opções deve ser escolhida. "Centro de custo" ou "Centro de receita"'
            )

        return data

    class Meta:
        model = models.ClassificationCenter
        fields = '__all__'
