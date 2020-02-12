from django.contrib import admin

from conttudoweb.purchase.models import PurchaseOrder, PurchaseItems


class PurchaseItemsInline(admin.TabularInline):
    model = PurchaseItems
    extra = 0
    autocomplete_fields = ['product']


@admin.register(PurchaseOrder)
class PurchaseOrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'code', 'date']
    list_display_links = ['id', 'supplier']
    autocomplete_fields = ['supplier']
    inlines = [PurchaseItemsInline]
    ordering = ['-date']
