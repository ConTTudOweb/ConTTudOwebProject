from django.contrib import admin

from conttudoweb.accounting.admin import AccountReceivablesModelForm
from conttudoweb.accounting.models import AccountReceivables, Account
from conttudoweb.sale.models import SaleOrder, SaleOrderItems


class SaleOrderItemsInline(admin.TabularInline):
    model = SaleOrderItems
    extra = 1
    autocomplete_fields = ['product']
    readonly_fields = ('amount',)


from django import forms
class AccountReceivablesSaleOrderModelForm(AccountReceivablesModelForm):
    type = forms.ChoiceField(choices=AccountReceivables.TYPE_CHOICES_INLINES)

    def __init__(self, *args, **kwargs):
        super(AccountReceivablesSaleOrderModelForm, self).__init__(*args, **kwargs)
        if self.instance.pk and (self.instance.type != Account.AccountTypes.normal.value):
            self.fields['frequency'].disabled = True
            self.fields['number_of_parcels'].disabled = True

    class Meta(AccountReceivablesModelForm.Meta):
        fields = ('type', 'frequency', 'number_of_parcels', 'due_date', 'amount', 'expected_deposit_account',
                  'document')


class AccountReceivablesInline(admin.TabularInline):
    model = AccountReceivables
    extra = 0
    form = AccountReceivablesSaleOrderModelForm

    # def get_readonly_fields(self, request, obj=None):
    #     _readonly_fields = super(AccountReceivablesInline, self).get_readonly_fields(self)
    #     print(obj)
    #     # if obj.type == self.model.AccountTypes.parcelled.value:
    #     #     _readonly_fields += ['frequency', 'number_of_parcels']
    #     return _readonly_fields


@admin.register(SaleOrder)
class SaleOrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'code', 'date']
    list_display_links = ['id', 'customer']
    autocomplete_fields = ['customer']
    inlines = [SaleOrderItemsInline, AccountReceivablesInline]
    ordering = ['-date']
    readonly_fields = ('amount',)
    fieldsets = (
        (None, {'fields': (('customer', 'date'), ('code', 'amount'))}),
    )
