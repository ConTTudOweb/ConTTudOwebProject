from django.contrib import admin

from conttudoweb.inventory.models import Product, ProductBySupplier, Category, Subcategory, UnitOfMeasure, \
    ProductSizeRegister, ProductSize, Stock


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


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 0


@admin.register(ProductSizeRegister)
class ProductSizeRegisterModelAdmin(admin.ModelAdmin):
    inlines = [ProductSizeInline]
    search_fields = ['description']


@admin.register(ProductSize)
class ProductSizeModelAdmin(admin.ModelAdmin):
    search_fields = ['description']
    autocomplete_fields = ['product_size_register']
    list_filter = ['product_size_register']


@admin.register(UnitOfMeasure)
class UnitOfMeasureModelAdmin(admin.ModelAdmin):
    list_display = ['initials', 'description']
    ordering = ['initials']


class ProductBySupplierInline(admin.TabularInline):
    model = ProductBySupplier
    extra = 0
    autocomplete_fields = ['supplier']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'unit_of_measure', 'ncm', 'subcategory', 'last_cost_price']
    search_fields = ['code', 'description', 'ncm', 'productbysupplier__description']
    inlines = [ProductBySupplierInline]
    autocomplete_fields = ['subcategory']


@admin.register(Stock)
class StockModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
