from django.contrib import admin

from conttudoweb.accounting.forms import AccountPayablePurchaseOrderModelForm
from conttudoweb.accounting.models import AccountPayable
from conttudoweb.core import utils
from conttudoweb.purchase.models import PurchaseOrder, PurchaseItems


class PurchaseItemsInline(admin.TabularInline):
    model = PurchaseItems
    extra = 0
    autocomplete_fields = ['product']


class AccountPayableInline(admin.TabularInline):
    model = AccountPayable
    extra = 0
    form = AccountPayablePurchaseOrderModelForm


@admin.register(PurchaseOrder)
class PurchaseOrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'code', 'date', 'amount_total_admin']
    list_display_links = ['id', 'supplier']
    list_filter = (('supplier', admin.RelatedOnlyFieldListFilter), 'date')
    date_hierarchy = 'date'
    autocomplete_fields = ['supplier']
    inlines = [PurchaseItemsInline, AccountPayableInline]
    ordering = ['-date']
    fieldsets = (
        ('Geral', {'fields': ('supplier', ('date', 'code'), 'amount_total_admin')}),
    )
    readonly_fields = ('amount_total_admin',)

    def amount_total_admin(self, obj):
        return utils.format_currency(obj.amount_total)
    amount_total_admin.short_description = 'Valor total'
