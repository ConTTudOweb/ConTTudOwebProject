from django import forms
from django.contrib import admin

from .models import AccountReceivables, AccountPayable, Bank, Category, ClassificationCenter, DepositAccount


class AccountModelForm(forms.ModelForm):
    class Media:
        js = ('js/account-type-field-admin.js',)


class AccountPayableModelForm(AccountModelForm):
    class Meta:
        labels = {
            'expected_deposit_account': 'Pagar por',
        }


class AccountReceivablesModelForm(AccountModelForm):
    class Meta:
        labels = {
            'expected_deposit_account': 'Receber por',
        }


class AccountModelAdmin:
    list_display = ('description', 'due_date', 'amount', 'category', 'person')
    search_fields = ('description',)
    exclude = ('entity',)
    autocomplete_fields = ('category',)
    raw_id_fields = ('person',)  # TODO: autocomplete_fields não está funcionando com limit_choices_to
    fieldsets = (
        (None, {
            'fields': (('type', 'frequency', 'number_of_parcels'),
                       ('description', 'due_date', 'amount'),
                       ('category', 'document_emission_date', 'expected_deposit_account'),
                       ('person', 'classification_center', 'document'),
                       'observation')
        }),
    )
    radio_fields = {"type": admin.HORIZONTAL}

    def save_model(self, request, obj, form, change):
        obj.entity = request.user.entity
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(entity=request.user.entity)


@admin.register(AccountPayable)
class AccountPayableModelAdmin(AccountModelAdmin, admin.ModelAdmin):
    form = AccountPayableModelForm


@admin.register(AccountReceivables)
class AccountReceivablesModelAdmin(AccountModelAdmin, admin.ModelAdmin):
    form = AccountReceivablesModelForm


@admin.register(Bank)
class BankModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)


@admin.register(ClassificationCenter)
class ClassificationCenterModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    exclude = ('entity',)
    fields = ('name', ('cost_center', 'revenue_center'))

    def save_model(self, request, obj, form, change):
        obj.entity = request.user.entity
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(entity=request.user.entity)


class DepositAccountModelForm(forms.ModelForm):
    class Media:
        js = ('js/deposit-account-type-field-admin.js',)


@admin.register(DepositAccount)
class DepositAccountModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    exclude = ('entity',)
    autocomplete_fields = ('bank',)
    radio_fields = {"type": admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': ('type',
                       'bank',
                       ('agency_number', 'agency_digit'),
                       ('account_number', 'account_digit'),
                       'name')
        }),
    )
    form = DepositAccountModelForm

    def save_model(self, request, obj, form, change):
        obj.entity = request.user.entity
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(entity=request.user.entity)
