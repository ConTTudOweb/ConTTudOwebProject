from django.contrib import admin
from django.utils.encoding import force_text

from conttudoweb.core.forms import PeopleForm
from .models import People, City, FederativeUnit


class DefaultListFilter(admin.SimpleListFilter):
    all_value = '_all'

    def default_value(self):
        raise NotImplementedError()

    def queryset(self, request, queryset):
        if self.parameter_name in request.GET and request.GET[self.parameter_name] == self.all_value:
            return queryset

        if self.parameter_name in request.GET:
            return queryset.filter(**{self.parameter_name: request.GET[self.parameter_name]})

        return queryset.filter(**{self.parameter_name: self.default_value()})

    def choices(self, cl):
        yield {
            'selected': self.value() == self.all_value,
            'query_string': cl.get_query_string({self.parameter_name: self.all_value}, []),
            'display': 'Todos(as)',
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup) or (
                        self.value() is None and force_text(self.default_value()) == force_text(lookup)
                ),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }


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
                'customer', 'supplier',
                'name',
                'person_type',
                ('federation_subscription_number', 'state_subscription_number'), ('phone', 'email'),
                'observation'
            )
        }),
        ('Endereço', {
            'classes': ('collapse',),
            'fields': ('zip_code', ('address', 'address_number'), ('complement', 'neighborhood'), 'city'),
        }),
        # (None, {
        #     'fields': ('observation',)
        # }),
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
