from django.contrib import admin

from conttudoweb.inventory.models import Product, ProductBySupplier, Category, Subcategory, UnitOfMeasure, \
    ProductSizeRegister, ProductSize, Stock, Packaging, PackagingType


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 0


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    # inlines = [SubcategoryInline]
    search_fields = ['description']


@admin.register(Subcategory)
class SubcategoryModelAdmin(admin.ModelAdmin):
    list_display = ('category', 'description')
    search_fields = ['description']
    autocomplete_fields = ['category']
    list_filter = ['category']


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 0


@admin.register(ProductSizeRegister)
class ProductSizeRegisterModelAdmin(admin.ModelAdmin):
    list_display = ('description',)
    inlines = [ProductSizeInline]
    search_fields = ['description']


@admin.register(ProductSize)
class ProductSizeModelAdmin(admin.ModelAdmin):
    list_display = ('product_size_register', 'description')
    search_fields = ['description']
    autocomplete_fields = ['product_size_register']
    list_filter = ['product_size_register']


@admin.register(UnitOfMeasure)
class UnitOfMeasureModelAdmin(admin.ModelAdmin):
    list_display = ['initials', 'description']
    ordering = ['initials']


@admin.register(PackagingType)
class PackagingTypeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']
    list_editable = ['description']


class ProductBySupplierInline(admin.TabularInline):
    model = ProductBySupplier
    extra = 0
    autocomplete_fields = ['supplier']
    classes = ['collapse']


class PackagingInline(admin.TabularInline):
    model = Packaging
    extra = 0
    classes = ['collapse']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'unit_of_measure', 'ncm', 'subcategory', 'cost_price_of_last_purchase']
    list_display_links = ['id', 'description']
    search_fields = ['code', 'description', 'ncm', 'productbysupplier__description']
    inlines = [ProductBySupplierInline, PackagingInline]
    autocomplete_fields = ['subcategory']
    fieldsets = (
        (None, {
            'fields': (
                'description',
                ('unit_of_measure', 'code', 'ncm'),
                ('subcategory', 'product_size_register'),
                ('cost_price', 'sale_price', 'wholesale_selling_price'),
            )
        }),
    )


@admin.register(Stock)
class StockModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
