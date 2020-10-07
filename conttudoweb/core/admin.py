from django.contrib import admin

from conttudoweb.core.forms import PeopleForm
from .models import People, City, FederativeUnit


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
    list_display = ('name', 'observation')
    search_fields = ('name', 'observation')
    ordering = ['name']
    list_filter = ('customer', 'supplier')
    autocomplete_fields = ('city',)
    radio_fields = {'person_type': admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': (
            ('customer', 'supplier', 'person_type'), 'name', ('federation_subscription_number', 'state_subscription_number'), ('phone', 'email'))
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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            if 'accountpayable' in request.META.get('HTTP_REFERER', ''):
                queryset = queryset.filter(supplier=True)
            elif 'accountreceivable' in request.META.get('HTTP_REFERER', ''):
                queryset = queryset.filter(customer=True)
        return queryset, use_distinct
