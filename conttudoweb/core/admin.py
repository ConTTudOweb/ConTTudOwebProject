from django.contrib import admin
from django.conf import settings

from .models import People, City

admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.index_title = settings.ADMIN_INDEX_TITLE


# @admin.register(Entity)
# class EntityModelAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)


@admin.register(City)
class CityModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'uf')
    search_fields = ('name',)
    list_filter = ('uf',)


@admin.register(People)
class PeopleModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    # exclude = ('entity',)
    list_filter = ('customer', 'supplier')
    autocomplete_fields = ('city',)
    radio_fields = {'person_type': admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': (
            ('customer', 'supplier'), 'name', 'person_type', 'federation_subscription_number', 'phone', 'email')
        }),
        ('Endereço', {
            'classes': ('collapse',),
            'fields': ('zip_code', ('address', 'address_number'), ('complement', 'neighborhood'), 'city'),
        }),
        (None, {
            'fields': ('observation',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.entity = request.user.entity
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(entity=request.user.entity)
