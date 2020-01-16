from django.contrib import admin

from conttudoweb.inventory.models import Product, ProductBySupplier


class ProductBySupplierInline(admin.TabularInline):
    model = ProductBySupplier
    extra = 0
    autocomplete_fields = ['supplier']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    search_fields = ['code', 'description', 'ncm']
    inlines = [ProductBySupplierInline]
