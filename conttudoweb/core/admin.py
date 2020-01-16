from django.contrib import admin

from conttudoweb.core.forms import PeopleForm
from .models import People, City, FederativeUnit


# @admin.register(Entity)
# class EntityModelAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)


@admin.register(FederativeUnit)
class FederativeUnitModelAdmin(admin.ModelAdmin):
    list_display = ('initials', 'name')
    search_fields = ('initials', 'name')


@admin.register(City)
class CityModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'uf')
    search_fields = ('name',)
    list_filter = ('uf',)
    ordering = ['name']


@admin.register(People)
class PeopleModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']
    # exclude = ('entity',)
    list_filter = ('customer', 'supplier')
    autocomplete_fields = ('city',)
    radio_fields = {'person_type': admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': (
            ('customer', 'supplier'), ('name', 'person_type'), ('federation_subscription_number', 'state_subscription_number'), ('phone', 'email'))
        }),
        ('Endereço', {
            'classes': ('collapse',),
            'fields': ('zip_code', ('address', 'address_number'), ('complement', 'neighborhood'), 'city'),
        }),
        (None, {
            'fields': ('observation',)
        }),
    )
    form = PeopleForm

    # def save_model(self, request, obj, form, change):
    #     obj.entity = request.user.entity
    #     super().save_model(request, obj, form, change)

    # def get_queryset(self, request):
    #     return super().get_queryset(request).filter(entity=request.user.entity)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        print(request.path)
        if 'autocomplete' in request.path:
            queryset = queryset.filter(supplier=True)
        return queryset, use_distinct
