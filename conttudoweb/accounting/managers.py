from django.db import models

from conttudoweb.accounting.utils import AccountPaymentReceivement


class AccountReceivableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(payment_receivement=AccountPaymentReceivement.receivement.value, financial_movement=False)


class AccountPayableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(payment_receivement=AccountPaymentReceivement.payment.value, financial_movement=False)


class FinancialMovementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(liquidated=True)
