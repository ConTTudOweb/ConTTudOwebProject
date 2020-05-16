from django.contrib import admin

from conttudoweb.sale.models import SaleOrder, SaleOrderItems


class SaleOrderItemsInline(admin.TabularInline):
    model = SaleOrderItems
    extra = 1
    autocomplete_fields = ['product']
    readonly_fields = ('amount',)


@admin.register(SaleOrder)
class SaleOrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'code', 'date']
    list_display_links = ['id', 'customer']
    autocomplete_fields = ['customer']
    inlines = [SaleOrderItemsInline]
    ordering = ['-date']
    readonly_fields = ('amount',)
    fieldsets = (
        (None, {'fields': ('customer', 'code', 'date', 'amount')}),
    )
