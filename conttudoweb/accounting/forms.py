from django import forms

from conttudoweb.accounting.models import Account


class AccountModelForm(forms.ModelForm):
    class Media:
        # TODO: Criar um teste para verificar se o código do JS está funcionando.
        js = ('js/account-type-field-admin.js',)


class AccountPayableModelForm(AccountModelForm):
    class Meta:
        labels = {
            'expected_deposit_account': 'Pagar por',
            'person': 'Fornecedor',
            'classification_center': 'Centro de custo'
        }


class AccountReceivableModelForm(AccountModelForm):
    class Meta:
        labels = {
            'expected_deposit_account': 'Receber por',
            'person': 'Cliente',
            'classification_center': 'Centro de receita'
        }


class AccountInlineModelFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['type'].disabled = True
            if self.instance.type != Account.AccountTypes.normal.value:
                self.fields['frequency'].disabled = True
                self.fields['number_of_parcels'].disabled = True

    meta_fields = (
        'type', 'frequency', 'number_of_parcels', 'due_date', 'amount', 'expected_deposit_account', 'document'
    )


class AccountReceivableSaleOrderModelForm(AccountInlineModelFormMixin, AccountReceivableModelForm):
    type = forms.ChoiceField(choices=Account.TYPE_CHOICES_INLINES)

    class Meta(AccountReceivableModelForm.Meta):
        fields = AccountInlineModelFormMixin.meta_fields


class AccountPayablePurchaseOrderModelForm(AccountInlineModelFormMixin, AccountPayableModelForm):
    type = forms.ChoiceField(choices=Account.TYPE_CHOICES_INLINES)

    class Meta(AccountPayableModelForm.Meta):
        fields = AccountInlineModelFormMixin.meta_fields
