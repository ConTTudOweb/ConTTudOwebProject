from django import forms
from django.contrib import admin

from conttudoweb.accounting.admin import AccountReceivableModelForm
from conttudoweb.accounting.models import AccountReceivable, Account
from conttudoweb.sale.models import SaleOrder, SaleOrderItems, Vendor


@admin.register(Vendor)
class VendorModelAdmin(admin.ModelAdmin):
    pass


class SaleOrderItemsInline(admin.TabularInline):
    model = SaleOrderItems
    extra = 1
    autocomplete_fields = ['product']
    readonly_fields = ('amount',)


class AccountReceivableSaleOrderModelForm(AccountReceivableModelForm):
    type = forms.ChoiceField(choices=AccountReceivable.TYPE_CHOICES_INLINES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and (self.instance.type != Account.AccountTypes.normal.value):
            self.fields['frequency'].disabled = True
            self.fields['number_of_parcels'].disabled = True

    class Meta(AccountReceivableModelForm.Meta):
        fields = ('type', 'frequency', 'number_of_parcels', 'due_date', 'amount', 'expected_deposit_account',
                  'document')


class AccountReceivableInline(admin.TabularInline):
    model = AccountReceivable
    extra = 0
    form = AccountReceivableSaleOrderModelForm

    # def get_readonly_fields(self, request, obj=None):
    #     _readonly_fields = super(AccountReceivablesInline, self).get_readonly_fields(self)
    #     print(obj)
    #     # if obj.type == self.model.AccountTypes.parcelled.value:
    #     #     _readonly_fields += ['frequency', 'number_of_parcels']
    #     return _readonly_fields


# TODO: Criar travas no pedido para impedir a alteração após o fechamento do mesmo.
# TODO: Criar travas no receber do pedido para impedir o lançamento acima do valor do pedido.
# TODO: Criar impressão do pedido.
# TODO: Ao lançar o produto sugerir o preço de venda do mesmo.
@admin.register(SaleOrder)
class SaleOrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'code', 'date']
    list_display_links = ['id', 'customer']
    autocomplete_fields = ['customer']
    inlines = [SaleOrderItemsInline, AccountReceivableInline]
    ordering = ['-date']
    readonly_fields = ('amount',)
    fieldsets = (
        (None, {'fields': (('customer', 'date'), ('code', 'amount'))}),
    )
