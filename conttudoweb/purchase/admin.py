from django.contrib import admin

from conttudoweb.core import utils
from conttudoweb.purchase.models import PurchaseOrder, PurchaseItems


class PurchaseItemsInline(admin.TabularInline):
    model = PurchaseItems
    extra = 0
    autocomplete_fields = ['product']


@admin.register(PurchaseOrder)
class PurchaseOrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'code', 'date', 'amount_total_admin']
    list_display_links = ['id', 'supplier']
    autocomplete_fields = ['supplier']
    inlines = [PurchaseItemsInline]
    ordering = ['-date']
    fieldsets = (
        (None, {'fields': ('supplier', ('date', 'code'), 'amount_total_admin')}),
    )
    readonly_fields = ('amount_total_admin',)

    def amount_total_admin(self, obj):
        return utils.format_currency(obj.amount_total)
    amount_total_admin.short_description = 'Valor total'
