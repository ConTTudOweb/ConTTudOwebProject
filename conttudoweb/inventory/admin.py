from django.contrib import admin

from conttudoweb.inventory.models import Product, ProductBySupplier, Category, Subcategory


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 0


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]
    search_fields = ['description']


@admin.register(Subcategory)
class SubcategoryModelAdmin(admin.ModelAdmin):
    search_fields = ['description']
    autocomplete_fields = ['category']
    list_filter = ['category']


class ProductBySupplierInline(admin.TabularInline):
    model = ProductBySupplier
    extra = 0
    autocomplete_fields = ['supplier']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    search_fields = ['code', 'description', 'ncm']
    inlines = [ProductBySupplierInline]
    autocomplete_fields = ['subcategory']
