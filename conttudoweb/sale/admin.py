from django import forms
from django.contrib import admin

from conttudoweb.accounting.admin import AccountReceivableModelForm
from conttudoweb.accounting.models import AccountReceivable, Account
from conttudoweb.core import utils
from conttudoweb.sale.models import SaleOrder, SaleOrderItems


class SaleOrderItemsInline(admin.TabularInline):
    model = SaleOrderItems
    extra = 1
    autocomplete_fields = ['product']
    readonly_fields = ('amount',)


class AccountReceivableSaleOrderModelForm(AccountReceivableModelForm):
    type = forms.ChoiceField(choices=AccountReceivable.TYPE_CHOICES_INLINES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['type'].disabled = True
            if self.instance.type != Account.AccountTypes.normal.value:
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
    list_display = ['id', 'customer', 'date_order', 'discount_percentage', 'net_total_admin']
    list_display_links = ['id', 'customer']
    list_filter = (('customer', admin.RelatedOnlyFieldListFilter), 'date_order')
    date_hierarchy = 'date_order'
    autocomplete_fields = ['customer']
    inlines = [SaleOrderItemsInline, AccountReceivableInline]
    ordering = ['-date_order']
    readonly_fields = ('net_total_admin',)
    fieldsets = (
        ('Geral', {'fields': (('customer', 'date_order'), ('validity_date', 'discount_percentage'), 'net_total_admin')}),
    )

    def net_total_admin(self, obj):
        return utils.format_currency(obj.net_total)
    net_total_admin.short_description = 'Valor líquido'
