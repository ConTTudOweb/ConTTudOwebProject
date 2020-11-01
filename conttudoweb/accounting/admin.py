from decimal import Decimal

from django import forms
from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.db.models import Q, Sum, Window, F, Case, When, DecimalField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import resolve
from django.utils.html import format_html

from conttudoweb.accounting.utils import AccountPaymentReceivement
from .forms import AccountPayableModelForm, AccountReceivableModelForm, AccountModelForm
from .models import AccountReceivable, AccountPayable, Bank, Category, ClassificationCenter, DepositAccount, \
    Account, FinancialMovement, ExpectedCashFlow
from ..core.admin import DefaultListFilter


class ExpectedDepositAccountFilter(SimpleListFilter):
    title = DepositAccount._meta.verbose_name
    parameter_name = 'expected_deposit_account'

    def lookups(self, _, model_admin):
        return [(deposit_account.id, str(deposit_account)) for deposit_account in DepositAccount.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(expected_deposit_account__id__exact=self.value())
        else:
            messages.add_message(request, messages.WARNING, 'Escolha uma ' + self.title)
            return queryset.filter(expected_deposit_account__id__exact=0)


class LiquidatedFilter(DefaultListFilter):
    title = 'liquidado?'
    parameter_name = 'liquidated__exact'

    def lookups(self, request, model_admin):
        return (
            (True, 'Liquidado'),
            (False, 'Não Liquidado'),
        )

    def default_value(self):
        return False


class AccountModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'person', 'expected_deposit_account', 'amount', 'liquidated_date',
                    'liquidated')
    list_editable = ('expected_deposit_account', 'amount', 'liquidated_date', 'liquidated')
    search_fields = ('description', 'document')
    list_filter = (LiquidatedFilter, ('category', admin.RelatedOnlyFieldListFilter), 'expected_deposit_account',
                   ('person', admin.RelatedOnlyFieldListFilter))
    date_hierarchy = 'due_date'
    autocomplete_fields = ('category', 'person')
    fieldsets = (
        ('Geral', {
            'fields': (
                'type', ('frequency', 'number_of_parcels'),
                'description', ('due_date', 'amount'),
                ('document_emission_date', 'expected_deposit_account'),
                ('person', 'document'),
                ('category', 'classification_center'),
                'observation'
            )
        }),
    )
    radio_fields = {"type": admin.HORIZONTAL}
    ordering = ['due_date']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'POST':
            # TODO: Ao liquidar um título exigir que o mesmo tenha a conta financeira informada.
            if '_process' in request.POST:
                obj = self.model.objects.get(pk=object_id)
                obj.liquidated = not obj.liquidated
                obj.save()
                if obj.liquidated:
                    msg = "Baixa efetuada '{}'."
                else:
                    msg = "Estorno efetuado '{}'."
                self.message_user(
                    request,
                    msg.format(str(obj)),
                    messages.SUCCESS)
                return HttpResponseRedirect("../")

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def has_change_permission(self, request, obj=None):
        if obj:
            return super().has_change_permission(request, obj) and (not obj.liquidated)
        else:
            return super().has_change_permission(request, obj)

    class Media:
        js = ('js/account-list-admin.js',)
        css = {
            'all': ('css/account-list-admin.css',)
        }


# @admin.register(Recurrence)
# class RecurrenceModelAdmin(admin.ModelAdmin):
#     pass


@admin.register(AccountPayable)
class AccountPayableModelAdmin(AccountModelAdmin):
    form = AccountPayableModelForm
    change_form_template = 'change_form_accountPayable.html'


@admin.register(AccountReceivable)
class AccountReceivableModelAdmin(AccountModelAdmin):
    form = AccountReceivableModelForm
    change_form_template = 'change_form_accountReceivable.html'


class FinancialMovementModelForm(AccountModelForm):
    class Meta:
        labels = {
            'liquidated_date': 'Data do movimento'
        }


# TODO: Implementar transferencia entre contas
@admin.register(FinancialMovement)
class FinancialMovementModelAdmin(admin.ModelAdmin):
    class ExpectedDepositAccountFilter(SimpleListFilter):
        title = DepositAccount._meta.verbose_name
        parameter_name = 'expected_deposit_account'

        def lookups(self, _, model_admin):
            return [(deposit_account.id, str(deposit_account)) for deposit_account in DepositAccount.objects.all()]

        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(expected_deposit_account__id__exact=self.value())
            else:
                messages.add_message(request, messages.WARNING, 'Escolha uma ' + self.title)
                return queryset.filter(expected_deposit_account__id__exact=0)

    list_display = ('liquidated_date', 'title', 'person', 'amount_with_sign')
    list_filter = (ExpectedDepositAccountFilter,)
    search_fields = ('description',)
    date_hierarchy = 'liquidated_date'
    ordering = ('-liquidated_date',)
    actions_on_top = False
    actions_on_bottom = True

    autocomplete_fields = ('category',)
    raw_id_fields = ('person',)  # TODO: autocomplete_fields não está funcionando com limit_choices_to
    fieldsets = (
        ('Geral', {
            'fields': (
                'payment_receivement',
                ('description', 'liquidated_date', 'amount'),
                ('category', 'document_emission_date', 'expected_deposit_account'),
                ('person', 'classification_center', 'document'),
                'observation'
            )
        }),
    )
    radio_fields = {"payment_receivement": admin.HORIZONTAL}

    form = FinancialMovementModelForm
    change_list_template = 'change_list_financial_movement.html'

    def amount_with_sign(self, obj):
        _css_class = 'positive-value'
        if obj.amount_with_sign < 0:
            _css_class = 'negative-value'
        return format_html(
            '<span class="{}">{}</span>', _css_class, obj.amount_with_sign
        )

    amount_with_sign.admin_order_field = 'amount_with_sign'
    amount_with_sign.short_description = Account.amount_label
    amount_with_sign.allow_tags = True

    def has_add_permission(self, request):
        if resolve(request.path_info).url_name == 'accounting_financialmovement_changelist':
            return request.GET.get('expected_deposit_account', None) and super().has_add_permission(request)
        elif resolve(request.path_info).url_name == 'accounting_financialmovement_add':
            return request.session.get('expected_deposit_account', None) and super().has_add_permission(request)

    def changelist_view(self, request, extra_context=None):
        expected_deposit_account = request.GET.get('expected_deposit_account', None)
        if expected_deposit_account is not None:
            deposit_account = DepositAccount.objects.get(id=expected_deposit_account)
            extra_context = {'deposit_account': deposit_account, **(extra_context or {})}
            request.session['expected_deposit_account'] = expected_deposit_account
        return super().changelist_view(request, extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'expected_deposit_account':
            kwargs['initial'] = request.session.get('expected_deposit_account', None)
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial = {
            'expected_deposit_account': request.session.get('expected_deposit_account', None),
            'payment_receivement': AccountPaymentReceivement.payment.value,
            **initial
        }
        return initial

    class Media:
        js = ('js/financial-movement-admin.js',)


@admin.register(Bank)
class BankModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('description',)


@admin.register(ClassificationCenter)
class ClassificationCenterModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    # exclude = ('entity',)
    fields = ('name', ('cost_center', 'revenue_center'))

    # def save_model(self, request, obj, form, change):
    #     obj.entity = request.user.entity
    #     super().save_model(request, obj, form, change)

    # def get_queryset(self, request):
    #     return super().get_queryset(request).filter(entity=request.user.entity)


class DepositAccountModelForm(forms.ModelForm):
    class Media:
        js = ('js/deposit-account-type-field-admin.js',)


@admin.register(DepositAccount)
class DepositAccountModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')
    search_fields = ('name',)
    # exclude = ('entity',)
    autocomplete_fields = ('bank',)
    radio_fields = {"type": admin.HORIZONTAL}
    fieldsets = (
        ('Geral', {
            'fields': ('type',
                       'bank',
                       ('agency_number', 'agency_digit'),
                       ('account_number', 'account_digit'),
                       'name')
        }),
    )
    form = DepositAccountModelForm

    # def balance(self, obj):
    #     return obj.balance()


class CustomForm(forms.Form):
    expected_deposit_account = forms.ModelMultipleChoiceField(queryset=DepositAccount.objects.all(), required=False,
                                                              label='Conta financeira',
                                                              widget=forms.CheckboxSelectMultiple)
    start_date = forms.DateField(widget=forms.SelectDateWidget, required=False, label='Vencimento inicial')
    end_date = forms.DateField(widget=forms.SelectDateWidget, required=False, label='Vencimento final')

    def selected_expected_deposit_account_labels(self):
        return [
            label for value, label in self.fields['expected_deposit_account'].choices
            if str(value) in self['expected_deposit_account'].value()
        ]


@admin.register(ExpectedCashFlow)
class ExpectedCashFlowModelAdmin(admin.ModelAdmin):
    change_list_template = 'change_form_expected_cash_flow.html'

    def has_add_permission(*args, **kwargs):
        return False

    def has_change_permission(*args, **kwargs):
        return True

    def has_delete_permission(*args, **kwargs):
        return False

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['form'] = CustomForm()
        extra_context['empty_value_display'] = self.admin_site.empty_value_display

        result = super(ExpectedCashFlowModelAdmin, self).changelist_view(request, extra_context)
        context = result.context_data
        # context = {
        #     **self.admin_site.each_context(request),
        #     'title': self.model._meta.verbose_name_plural,
        #     'opts': ExpectedCashFlow._meta,
        #     'empty_value_display': self.admin_site.empty_value_display
        # }
        if request.method == 'POST':
            form = CustomForm(request.POST)
            if form.is_valid():
                _filter = Q(liquidated=False)
                _filter &= (Q(expected_deposit_account__in=form.cleaned_data['expected_deposit_account']) | Q(
                    expected_deposit_account__isnull=True))
                if form.cleaned_data['start_date'] is not None:
                    _filter &= Q(due_date__gte=form.cleaned_data['start_date'])
                if form.cleaned_data['end_date'] is not None:
                    _filter &= Q(due_date__lte=form.cleaned_data['end_date'])

                opening_balance = Decimal(0)
                for i in DepositAccount.objects.filter(id__in=form['expected_deposit_account'].value()):
                    opening_balance += i.balance()

                transactions = Account.objects.filter(_filter).annotate(
                    cumulative_amount=Window(
                        Sum(
                            Case(
                                When(payment_receivement=AccountPaymentReceivement.payment.value,
                                     then=(F('amount') * -1)),
                                default=F('amount'),
                                output_field=DecimalField()
                            )
                        ),
                        order_by=(
                            F('due_date').asc(),
                            F('id').asc()
                        )
                    ) + opening_balance,
                ).order_by('due_date', 'id')

                context['queryset'] = transactions
                context['form'] = form
                context['opening_balance'] = opening_balance
                return render(request, 'rel_expected_cash_flow.html', context)
        # else:
        #     form = CustomForm()

        return result
        # context['form'] = form
        # return render(request, 'change_form_expected_cash_flow.html', context)
