from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import AccountReceivables, AccountPayable, Bank, Category, ClassificationCenter, DepositAccount


class AccountModelForm(forms.ModelForm):
    class Media:
        js = ('js/account-type-field-admin.js',)
        # TODO: Criar um teste para verificar se o código do JS acima está funcionando.


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
    list_display = ('description', 'due_date', 'amount', 'category', 'person', 'action')
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

    def action(self, obj):
        text = None
        url_reverse = None
        _reconcile = "Conciliar"
        _reconciled = "Conciliado"

        if self.__class__ == AccountPayableModelAdmin:
            if not obj.liquidated:
                text = "Pagar"
                url_reverse = "admin:accounting_accountpayable_change"
            elif not obj.reconciled:
                text = _reconcile
                url_reverse = "admin:accounting_accountpayable_change"
            elif obj.reconciled:
                text = _reconciled
                url_reverse = "admin:accounting_accountpayable_change"
        elif self.__class__ == AccountReceivablesModelAdmin:
            if not obj.liquidated:
                text = "Receber"
                url_reverse = "admin:accounting_accountreceivables_change"
            elif not obj.reconciled:
                text = _reconcile
                url_reverse = "admin:accounting_accountreceivables_change"
            elif obj.reconciled:
                text = _reconciled
                url_reverse = "admin:accounting_accountreceivables_change"

        if text is not None:
            return format_html(
                '<a class="button" href="{}">'+text+'</a>',
                reverse(url_reverse, args=[obj.pk]),
            )
        else:
            return ""

    action.short_description = ''
    action.allow_tags = True


@admin.register(AccountPayable)
class AccountPayableModelAdmin(AccountModelAdmin, admin.ModelAdmin):
    form = AccountPayableModelForm
    change_form_template = 'change_form_accountPayable.html'


@admin.register(AccountReceivables)
class AccountReceivablesModelAdmin(AccountModelAdmin, admin.ModelAdmin):
    form = AccountReceivablesModelForm
    change_form_template = 'change_form_accountReceivables.html'


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
